from django.urls import path
from . import  views
urlpatterns = [
	    path("assigntask<str:task_id>", views.assign_task, name="assigntask"),
	    path("event", views.event, name="event")
]