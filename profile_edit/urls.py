
from django.urls import path
from .views import profile_edit, person

urlpatterns = [
    path('profile/', profile_edit, name='profile'),
    path('person/', person, name='person'),
    
]