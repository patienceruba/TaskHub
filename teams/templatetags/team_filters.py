from django import template
from ..models import TeamMember

register = template.Library()

@register.filter
def is_admin(user, team):
    """
    Check if a user is an admin of the given team.
    """
    return TeamMember.objects.filter(user=user, team=team, is_admin=True).exists()
