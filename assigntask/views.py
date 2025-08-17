from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from todo.models import Task, SubTask
from .models import AssignedTask
import json
from django.utils import timezone
User = get_user_model()



@login_required
def event(request):
    now = timezone.now()
    assigned_tasks = AssignedTask.objects.filter(
        user=request.user,
        task__start_date__gte=now  # only future or ongoing tasks
    ).select_related('task')

    events = [
        {
            'title': task.task.title,
            'date': task.task.start_date.isoformat(),
            'end_date': task.task.end_date.isoformat() if task.task.end_date else None,
        }
        for task in assigned_tasks
    ]

    return render(request, 'assigntask/events.html', {
        'assigned_tasks': assigned_tasks,
        'events': json.dumps(events, cls=DjangoJSONEncoder),
    })



@login_required
def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    team = task.team
    team_users = User.objects.filter(teammember__team=team)
    subtasks = SubTask.objects.filter(record=task)

    if request.method == 'POST':
        user_id = request.POST.get('user')
        subtask_id = request.POST.get('subtask')

        user = get_object_or_404(User, id=user_id)
        subtask = get_object_or_404(SubTask, id=subtask_id, record=task)

        if user not in team_users:
            return HttpResponseForbidden("You can only assign tasks to team members.")

        # Create or get the assigned task
        assigned_task, created = AssignedTask.objects.get_or_create(user=user, task=task)

        # Set the subtask and save (only if newly created or needs update)
        if assigned_task.subtask != subtask:
            assigned_task.subtask = subtask
            assigned_task.save()

        return redirect('task_detail', pk=task.id)

    context = {
        'task': task,
        'users': team_users,
        'subtasks': subtasks,
    }
    return render(request, 'assigntask/assignuser.html', context)



@login_required
def progress_tracking(request):
    assigned_tasks = AssignedTask.objects.filter(user=request.user).select_related('task')

    task_progress = []
    for assigned in assigned_tasks:
        task = assigned.task
        subtasks = task.subtasks.all()

        total_subtasks = subtasks.count()
        completed_subtasks = subtasks.filter(done=True).count()
        progress = (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0

        task_progress.append({
            'task': task,
            'assigned': assigned,
            'total_subtasks': total_subtasks,
            'completed_subtasks': completed_subtasks,
            'progress_percentage': round(progress, 2),
        })

    total_tasks = len(task_progress)
    average_progress = (
        sum(item['progress_percentage'] for item in task_progress) / total_tasks
    ) if total_tasks > 0 else 0

    context = {
        'task_progress': task_progress,
        'total_tasks': total_tasks,
        'average_progress': round(average_progress, 2),
    }

    return render(request, 'tasks/progress_tracking.html', context)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    subtasks = SubTask.objects.filter(record=task)
    assigned_users = task.assignedtask_set.all()
    return render(request, 'assigntask/task_detail.html', {
        'task': task,
        'assigned_users': assigned_users,
        'subtasks': subtasks,
    })


def view_assigned_subtask(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    return render(request, "assigntask/assigned_events.html", {"subtask": subtask})


def assign_task_and_notify(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id)
    user = get_object_or_404(User, id=user_id)

    # Assign the task to the user
    task.assigned_to = user
    task.save()

    subject = f"New Task Assigned - {task.title}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    html_content = render_to_string('emails/task_assignment.html', {
        'user': user,
        'task': task,
        'assigned_by': request.user,
        'task_link': f"https://yourdomain.com/tasks/{task.id}/"
    })

    email = EmailMultiAlternatives(subject, '', from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('task_detail', task_id=task.id)
