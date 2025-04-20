
from django.urls import path
from .views import image

urlpatterns = [
    path('add_image/', image, name='add_image'),
]