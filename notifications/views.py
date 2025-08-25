# notifications/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

@api_view(['GET'])
def unread_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    serializer = NotificationSerializer(notifications, many=True)
    return Response({
        "unread_count": unread_count,
        "notifications": serializer.data
    })


@api_view(['PATCH'])
def mark_notification_read(request, pk):
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True  # corrected field name
        notification.save()
        return Response({"success": True})
    except Notification.DoesNotExist:
        return Response({"success": False}, status=404)
