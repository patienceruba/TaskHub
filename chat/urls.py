
from django.urls import path
from .views import chatapp, send_message

urlpatterns = [
    path('chat/<int:team_id>/', chatapp, name='chatapp'),
    path('send_message/<int:team_id>/', send_message, name='send_message'),
]