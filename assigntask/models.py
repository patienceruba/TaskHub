from django.db import models
from django.contrib.auth.models import User
from todo.models import RecordRow


class AssignedTask(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    task= models.ForeignKey(RecordRow, on_delete=models.CASCADE)
    progress = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} -> {self.task.title}"