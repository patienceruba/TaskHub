from django.shortcuts import render,get_object_or_404, redirect
from .models import AssignedTask
from todo.models import Task, SubTask
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings

@login_required
def event(request):
    assigned_tasks = AssignedTask.objects.filter(user=request.user).select_related('task')

    events = [
        {
            'title': task.task.title,
            'date': task.task.start_date.isoformat(),  # 
            'end_date': task.task.end_date.isoformat() if task.task.end_date else None,
        }
        for task in assigned_tasks
    ]

    return render(request, 'assigntask/events.html', {
        'assigned_tasks': assigned_tasks,
        'events': json.dumps(events, cls=DjangoJSONEncoder),
    })

"""def assign_task(request, task_id,pk):
    task = get_object_or_404(Task, id=task_id)
    assigned_task = AssignedTask.objects.get(pk=pk)
    team = task.team  
    
    # Get User objects, not TeamMember objects
    users = User.objects.filter(teammember__team=team)

    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = get_object_or_404(User, id=user_id)

        if user not in users:
            return HttpResponseForbidden("You can only assign tasks to team members.")

        if not AssignedTask.objects.filter(user=user, task=task).exists():
            AssignedTask.objects.create(user=user, task=task)
        
        return redirect('task_detail', pk=task.id)

    return render(request, 'assigntask/assignuser.html', {'task': task, 'users': users, "assign_task":assign_task})"""


def assign_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    team = task.team

    # Get users who are members of the task's team
    team_users = User.objects.filter(teammember__team=team)

    if request.method == 'POST':
        user_id = request.POST.get('user')
        user = get_object_or_404(User, id=user_id)

        if user not in team_users:
            return HttpResponseForbidden("You can only assign tasks to team members.")

        # Prevent duplicate assignment
        AssignedTask.objects.get_or_create(user=user, task=task)

        return redirect('task_detail', pk=task.id)

    context = {
        'task': task,
        'users': team_users,
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

    # Overall summary (optional)
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
    print("taskname: "+task.title)
    print(subtasks)
    return render(request, 'assigntask/task_detail.html', {
        'task': task,
        'assigned_users': assigned_users,
        'subtasks': subtasks,
    })


def view_assigned_subtask(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    return render(request, "assigntask/assigned_events.html", {"subtask": subtask})


  # Assuming you have a Task model

def assign_task_and_notify(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id)
    user = get_object_or_404(User, id=user_id)

    # Assign the task (your logic here)
    task.assigned_to = user
    task.save()

    # Email subject and sender
    subject = f"New Task Assigned - {task.title}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    # Render the HTML content
    html_content = render_to_string('emails/task_assignment.html', {
        'user': user,
        'task': task,
        'assigned_by': request.user,  # Or whoever is assigning the task
        'task_link': f"https://yourdomain.com/tasks/{task.id}/"
    })

    # Send email
    email = EmailMultiAlternatives(subject, '', from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('task_detail', task_id=task.id)
