# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Team

class ApproveUserForm(forms.Form):
    user_id = forms.IntegerField(label='User ID', min_value=1)
    team_id = forms.IntegerField(label='Team ID', min_value=1)

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")
        return user

    def clean_team_id(self):
        team_id = self.cleaned_data['team_id']
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise forms.ValidationError("Team does not exist.")
        return team

    def approve_and_add_user(self):
        user = self.cleaned_data['user_id']
        team = self.cleaned_data['team_id']

        # Check if the user is already a member of the team
        if TeamMembership.objects.filter(user=user, team=team).exists():
            raise forms.ValidationError(f"{user.username} is already a member of the team.")
        
        # Add user to the team as a member
        membership = TeamMembership.objects.create(user=user, team=team, approved=True)
        membership.save()
        return membership
