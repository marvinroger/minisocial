from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from .models import Message, MessageHistory

@login_required
@require_GET
def index(request):
    history = MessageHistory.objects.all().order_by('-id')

    messages = []
    last_state = history.latest('id').id
    for entry in history:
        if not entry.is_addition:
            continue

        messages.append({
            'id': entry.message.id,
            'username': entry.message.user.username,
            'message_text': entry.message.message_text,
            'pub_date': entry.message.pub_date,
        })

    return render(request, 'app/index.html', {'messages': messages, 'last_state': last_state})

@require_GET
def login(request):
    return render(request, 'app/login.html')

@require_GET
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
@require_POST
def post_message(request):
    message_arg = request.POST.get('message')

    if not message_arg:
        return redirect('/')

    message = Message(user=request.user, message_text=message_arg)
    message.save()
    MessageHistory(message=message, is_addition=True).save()

    return JsonResponse({'id': message.id, 'pub_date': message.pub_date})

@login_required
@require_GET
def get_activity(request):
    last_state_arg = request.GET.get('last_state')

    if not last_state_arg:
        return redirect('/')

    try:
        last_state_arg = int(last_state_arg)
    except ValueError:
        return redirect('/')

    feed = []
    last_state = last_state_arg
    try:
        history = MessageHistory.objects.filter(id__gt=int(last_state_arg))
        last_state = history.latest('id').id

        for entry in history:
            serialized = {'id': entry.message.id}
            if entry.is_addition:
                serialized['type'] = '+'
                serialized['username'] = entry.message.user.username
                serialized['message_text'] = entry.message.message_text
                serialized['pub_date'] = entry.message.pub_date
            else:
                serialized['type'] = '-'

            feed.append(serialized)
    except ObjectDoesNotExist:
        pass

    return JsonResponse({'feed': feed, 'last_state': last_state})
