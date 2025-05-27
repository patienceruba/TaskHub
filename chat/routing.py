from django.urls import path
from . import chatConsumers

websocket_urlpatterns = [
    path('ws/chat/<int:team_id>/', chatConsumers.ChatConsumer.as_asgi()),
]
