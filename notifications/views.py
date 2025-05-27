from .models import Notification
from django.shortcuts import render
from django.http import JsonResponse
from assigntask.models import AssignedTask


def assign_task_to_user(user, task):
    # Create an AssignedTask record
    AssignedTask.objects.create(user=user, task=task, progress="Not Started")

    # Create a notification for the user
    Notification.objects.create(
        user=user,
        message=f"A new task '{task.title}' has been assigned to you."
    )

def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})

