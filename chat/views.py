from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, Team  # Import the Message model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def chatapp(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        return render(request, 'chat/team_not_found.html', {'team_id': team_id})  # Render a custom template

    messages = Message.objects.filter(team=team).order_by('timestamp')  # Fetch messages for the team

    if request.method == 'POST':
        message_content = request.POST.get('message')  # Get the message content from the POST data
        if message_content:  # Check if the message is not empty
            # Create a new message instance
            Message.objects.create(
                content=message_content,
                sender=request.user,
                team=team
            )
            return redirect('chatapp', team_id=team.id)  # Redirect to the same chat room

    return render(request, 'chat/chat.html', {
        'team': team,
        'messages': messages,
        'team_id': team_id
    })


@login_required
def send_message(request, team_id):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            # Create a new message instance
            message = Message.objects.create(
                content=message_content,
                sender=request.user,
                team_id=team_id
            )
            # Return a JSON response with the new message data
            return JsonResponse({
                'message': message.content,
                'sender': message.sender.username,
                'timestamp': message.timestamp.isoformat()  # Assuming you have a timestamp field
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)