from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from todo.models import RecordRow, SubTask

class AssignedTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(
        RecordRow, 
        on_delete=models.CASCADE, 
        
    )
    subtask = models.ForeignKey(SubTask, on_delete=models.CASCADE)

    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Completion percentage (0–100)."
    )
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.task.title} → {self.subtask.title}"
