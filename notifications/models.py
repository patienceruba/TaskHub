from django.db import models
from django.conf import settings
from chat.models import Message

class Notification(models.Model):
    NOTIF_TYPE = [
        ('task', 'Task'),
        ('chat', 'Chat'),
        ('group', 'Group'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    type = models.CharField(max_length=20, choices=NOTIF_TYPE, default='task')
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.user.username}: {self.type} - {self.message.content[:20]}"
