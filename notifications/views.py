from django.http import JsonResponse
from .models import Notification
from assigntask.models import AssignedTask

def assign_task_to_user(user, task):
    # Assign the task
    AssignedTask.objects.create(user=user, task=task, progress="Not Started")

    # Create a notification
    Notification.objects.create(
        user=user,
        message=f"A new task '{task.title}' has been assigned to you."
    )

def get_notifications(request):
    if request.user.is_authenticated:
        # Fetch the most recent unread notifications (limit to 10)
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:10]

        # Format for JSON
        notifications_data = [
            {
                'message': notification.message,
                'timestamp': notification.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for notification in unread_notifications
        ]

        return JsonResponse({
            'unread_count': unread_notifications.count(),
            'notifications': notifications_data
        })

    return JsonResponse({
        'unread_count': 0,
        'notifications': []
    })
