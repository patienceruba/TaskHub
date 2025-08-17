from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home', views.home, name="home"),
    path("add", views.addRecord, name='add'),
    path("delete/<str:pk>/", views.deleteRow, name="delete"),
    path('update/<str:pk>/', views.updateRecord, name="update"),
    path("search", views.search, name="search"),
    path("calendar", views.calendar, name="calendar"),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('tasks/done/', views.task_done_view, name='task_done'),
    path('today', views.today_view, name="today"),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('reset_task_notification/', views.reset_task_notification, name='reset_task_notification'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'), 
    path("teamMembership", views.team_member_ship, name="teamMembership"),
    path('slider/', views.slider_view, name='slider_view'),
    path('record/<int:record_id>/subtask/create/', views.create_subtask, name='subtask_create'),
    path('total_task/', views.task_dashboard, name='total_task'),
    path("success/", views.success, name="success"),
    
   
]
