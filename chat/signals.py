from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    if created:
        # Get all team members except the sender
        team_members = instance.team.members.exclude(id=instance.sender.id)
        
        for user in team_members:
            # Create a notification
            notif = Notification.objects.create(
                user=user,
                message=instance,
                type='chat'
            )

            # Optionally push via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "message": f"New message from {instance.sender.username}: {instance.content}",
                    "notification_id": notif.id,
                }
            )
