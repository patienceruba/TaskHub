from django.urls import path
from . import views

urlpatterns = [
    # Teams
    path('teams/', views.list_teams, name='list_teams'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/<int:pk>/join/', views.join_team_request, name='join_team_request'),
    path('teams/<int:pk>/delete/', views.delete_team, name='delete_team'),

    # Manage Requests (Admin)
    path('teams/<int:team_id>/requests/', views.manage_requests, name='manage_requests'),
    path('requests/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('requests/<int:request_id>/reject/', views.reject_request, name='reject_request'),

    # Admin Dashboard
    path('admin/requests/', views.view_requests, name='view_requests'),

    # Team Member Management
    path('teams/<int:team_id>/remove/<int:member_id>/', views.remove_member, name='remove_member'),
]
