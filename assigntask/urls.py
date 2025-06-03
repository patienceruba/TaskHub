from django.urls import path
from . import  views
urlpatterns = [
	    
	    path("event", views.event, name="event"),
        
        path('task/<int:pk>/', views.task_detail, name='task_detail'),
    	path('assigntask/<int:task_id>/', views.assign_task, name='assign_task'),
        path("view_assigned_subtask/<int:pk>/", views.view_assigned_subtask, name="view_assigned_subtask"),


]