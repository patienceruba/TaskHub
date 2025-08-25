from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_notification(user, message, type='task', link=None):
    notif = Notification.objects.create(user=user, message=message, type=type, link=link)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "send_notification",
            "message": {
                "id": notif.id,
                "message": notif.message,
                "type": notif.type,
                "link": notif.link
            }
        }
    )
