
from django.urls import path
from .views import profile_edit, person,change_password, validate_password_done

urlpatterns = [
    path('profile/', profile_edit, name='profile'),
    path('person/', person, name='person'),
    path('change_passwd/', change_password, name='change_passwd'),
    path('password-change/done/', validate_password_done, name='password_change_done'),
]