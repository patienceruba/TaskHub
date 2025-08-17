# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('api/notifications/', views.get_notifications, name='api_notifications'),

]
