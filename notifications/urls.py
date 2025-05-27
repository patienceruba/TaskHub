from django.urls import path
from .views import assign_task_to_user, unread_notifications_count

urlpatterns = [
    path("notifications/assign/", assign_task_to_user, name = "notice"),
    path('notifications/unread-count/', unread_notifications_count, name='unread_notifications_count'),
]
