
from django.urls import path
from .views import image, add_image,delete_image

urlpatterns = [
    path('add_image/', add_image, name='add_image'),
    path('image', image, name="image"),
    path("delete/<str:pk>/", delete_image, name="delete")
]