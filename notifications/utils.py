from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification_to_user(user, message_text):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.id}',
        {
            'type': 'send_notification',
            'message': {'message': message_text}
        }
    )
