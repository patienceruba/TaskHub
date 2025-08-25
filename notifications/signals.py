# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from todo.models import Task   # ✅ import Task from todo app
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Task)
def task_notification(sender, instance, created, **kwargs):
    if created:
        message = f"New task assigned: {instance.title}"
    elif instance.completed:
        message = f"Task completed: {instance.title}"
    else:
        return

    Notification.objects.create(user=instance.assigned_to, message=message)

    # WebSocket push
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{instance.assigned_to.id}",
        {
            "type": "send_notification",
            "message": message,
        }
    )
