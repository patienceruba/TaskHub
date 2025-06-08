from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from teams.models import Team
from django.conf import settings



class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    progress = models.PositiveSmallIntegerField(default=0) 
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)    

    def save(self, *args, **kwargs):
        previous_done = self.done
        self.done = self.progress >= 100
        super().save(*args, **kwargs)

        # Create a TaskDone entry if just marked as done
        if self.done and not previous_done:
            TaskDone.objects.get_or_create(record=self, user=self.user)

    def __str__(self):
        return self.title

    def update_progress(self):
        total_subtasks = self.subtasks.count()
        if total_subtasks > 0:
            completed_subtasks = self.subtasks.filter(done=True).count()
            new_progress = int((completed_subtasks / total_subtasks) * 100)
        else:
            new_progress = 0

        if self.progress != new_progress or (self.progress == 100 and not self.done):
            self.progress = new_progress
            self.done = new_progress >= 100
            super().save(update_fields=['progress', 'done', 'updated_date'])

            if self.done:
                TaskDone.objects.get_or_create(record=self, user=self.user)


        
class TaskDone(models.Model):
    record = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='task_done')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task '{self.record.title}' completed by {self.user.username} on {self.completed_at}"



class PDFDocument(models.Model):
    record = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='pdf_documents')
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return f"{self.record.title} - {self.pdf.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    def __str__(self):
        return self.user.username

class SubTask(models.Model):
    record = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def save(self, *args, **kwargs):
        was_done = self.done
        super().save(*args, **kwargs)

        # Update the parent task's progress
        self.record.update_progress()

        # If the subtask is newly marked as done, check for all subtasks
        if self.done and not was_done:
            self.check_if_all_subtasks_done()

    def check_if_all_subtasks_done(self):
        # Mark the parent task as done if all subtasks are done
        if not self.record.subtasks.filter(done=False).exists():
            self.record.done = True
            self.record.save()

    def __str__(self):
        return f"{self.title}"





