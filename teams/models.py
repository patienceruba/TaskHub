from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)  # Add this line
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"

class TeamMemberRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=(("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")),
        default="Pending"
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "team")  # Prevent duplicate requests

    def __str__(self):
        return f"{self.user.username} requested to join {self.team.name}"
