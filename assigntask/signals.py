from django.db.models.signals import post_save
from django.dispatch import receiver
from ..todo.models import AssignedTask, RecordRow

@receiver(post_save, sender=AssignedTask)
def update_recordrow_progress(sender, instance, **kwargs):
    task = instance.task

    # Get all progress entries for this task
    assigned_tasks = AssignedTask.objects.filter(task=task)

    if assigned_tasks.exists():
        # Calculate average progress
        total_progress = sum([a.progress for a in assigned_tasks])
        avg_progress = total_progress // assigned_tasks.count()

        # Update the RecordRow
        task.progress = avg_progress
        task.save()
