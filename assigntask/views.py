from django.shortcuts import render,get_object_or_404, redirect
from .models import AssignedTask
from todo.models import RecordRow
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#********************************************************************************
#new changes instead of users to view all task he/she can view only assigned task.
#********************************************************************************


def event(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect if the user is not logged in

    # Fetch tasks assigned to the logged-in user
    assigned_tasks = AssignedTask.objects.filter(user=request.user)
    task = RecordRow.objects.filter(user=request.user)
    # Pass the queryset to the template
    return render(request, 'assigntask/events.html', {'assigned_tasks': assigned_tasks, 'tasks':task})


#********************************************************************************
#assigning task functionalities
#********************************************************************************

def assign_task(request, task_id):
    task = get_object_or_404(RecordRow, id=task_id)
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')  # Single-user assignment
        user = get_object_or_404(User, id=user_id)

        # Check if the user is already assigned to the task
        if not AssignedTask.objects.filter(user=user, task=task).exists():
            AssignedTask.objects.create(user=user, task=task)
        
        return redirect('task_detail', task_id=task.id)

    return render(request, 'assigntask/assignuser.html', {'task': task, 'users': users})

#********************************************************************************

@login_required
def progress_tracking(request):
    # Fetch assigned tasks for the logged-in user
    assigned_tasks = AssignedTask.objects.filter(user=request.user)

    # Optionally, calculate progress summary
    total_tasks = assigned_tasks.count()
    completed_tasks = assigned_tasks.filter(progress="Completed").count()
    progress_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        'assigned_tasks': assigned_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress_percentage': round(progress_percentage, 2),
    }

    return render(request, 'tasks/progress_tracking.html', context)