from django.urls import path
from .views import upload_task


urlpatterns = [
    path('', upload_task, name="upload-file")
]