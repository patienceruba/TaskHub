# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    message_content = serializers.CharField(source='message.content', read_only=True)  # get actual text

    class Meta:
        model = Notification
        fields = ['id', 'type', 'is_read', 'created_at', 'message_content']
