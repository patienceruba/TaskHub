from django.shortcuts import render,get_object_or_404, redirect
from .models import AssignedTask
from todo.models import RecordRow, SubTask
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.serializers.json import DjangoJSONEncoder
import json

@login_required
def event(request):
    assigned_tasks = AssignedTask.objects.filter(user=request.user).select_related('task')

    events = [
        {
            'title': task.task.title,
            'date': task.task.start_date.isoformat(),  # or other relevant start field
            'end_date': task.task.end_date.isoformat() if task.task.end_date else None,
        }
        for task in assigned_tasks
    ]

    return render(request, 'assigntask/events.html', {
        'assigned_tasks': assigned_tasks,
        'events': json.dumps(events, cls=DjangoJSONEncoder),
    })



def assign_task(request, task_id):
    task = get_object_or_404(RecordRow, id=task_id)
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')  # Single-user assignment
        user = get_object_or_404(User, id=user_id)

        # Check if the user is already assigned to the task
        if not AssignedTask.objects.filter(user=user, task=task).exists():
            AssignedTask.objects.create(user=user, task=task)
            return redirect('task_detail', pk=task.id)
        else:
            # Handle case if user is already assigned
            return redirect('task_detail', pk=task.id)

    return render(request, 'assigntask/assignuser.html', {'task': task, 'users': users})

@login_required

def progress_tracking(request):
    # Fetch only the tasks assigned to the current user
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
    # Get the task based on the pk
    task = get_object_or_404(RecordRow, pk=pk)
    
    # You can also add related data, for example, the users assigned to this task
    assigned_users = task.assignedtask_set.all()  # Assuming the relationship is via the AssignedTask model

    return render(request, 'assigntask/task_detail.html', {'task': task, 'assigned_users': assigned_users})
