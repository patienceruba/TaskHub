from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
#from django.contrib.auth.models import User
from django.conf import settings
from todo.models import Task, SubTask

class AssignedTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        
    )
    subtask = models.ForeignKey(SubTask, null=True, blank=True, on_delete=models.SET_NULL)


    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Completion percentage (0–100)."
    )
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        user = self.user.username if self.user else "Unknown User"
        task = self.task.title if self.task else "No Task"
        return f"{user} - {task}"
