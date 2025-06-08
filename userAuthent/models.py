# in your app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


JOB_ROLE_CHOICES = [
    ('developer', 'Developer'),
    ('designer', 'Designer'),
    ('analyst', 'System Analyst'),
    ('qa', 'Quality Assurance'),
    ('pm', 'Project Manager'),
    ('finance', 'Finance'),
    ('manage', 'Manager'),
    ('hr', 'HR Manager'),
]

class CustomUser(AbstractUser):
    job_role = models.CharField(max_length=50, choices=JOB_ROLE_CHOICES, blank=True, null=True)
