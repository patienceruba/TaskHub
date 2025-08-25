# notifications/urls.py
from django.urls import path
from .views import unread_notifications, mark_notification_read

urlpatterns = [
    path('unread-notifications/', unread_notifications, name='unread-notifications'),
    path('notifications/<int:pk>/mark-read/', mark_notification_read, name='mark-notification-read'),
]
