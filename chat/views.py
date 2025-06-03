from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message
from teams.models import Team


@login_required
def chat_room(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    messages = Message.objects.filter(team=team).order_by('timestamp')

    if request.method == 'POST':
        message_content = request.POST.get('message', '').strip()
        if message_content:
            Message.objects.create(
                content=message_content,
                sender=request.user,
                team=team
            )
            return redirect('chat_room', team_id=team.id)

    return render(request, 'chat/chat.html', {
        'team': team,
        'messages': messages,
    })


@login_required
def send_message_ajax(request, team_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        team = get_object_or_404(Team, id=team_id)
        message_content = request.POST.get('message', '').strip()

        if message_content:
            message = Message.objects.create(
                content=message_content,
                sender=request.user,
                team=team
            )
            return JsonResponse({
                'message': message.content,
                'sender': message.sender.username,
                'timestamp': message.timestamp.isoformat()
            })

    return JsonResponse({'error': 'Invalid request'}, status=400)
