from django.db import models
from django.contrib.auth.models import User
from teams.models import Team


# models.py

class Team(models.Model):
    name = models.CharField(max_length=100)
    # Other fields...

class Message(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username}: {self.content}'
    