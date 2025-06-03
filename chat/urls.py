from django.urls import path
from .views import chat_room, send_message_ajax

urlpatterns = [
    path('chat/<int:team_id>/', chat_room, name='chatapp'),
    #path('send_message/<int:team_id>/', send_message, name='send_message'),
]
