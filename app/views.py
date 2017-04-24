import json
from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.http import HttpResponse

from .models import Message, MessageHistory

@require_GET
def login(request):
    return render(request, 'app/login.html')

@require_GET
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
@require_GET
def index(request):
    messages = []
    last_state = 0
    try:
        history = MessageHistory.objects.all()

        messages = []
        last_state = history.latest('id').id
        for entry in history:
            if not entry.is_addition or entry.message.is_deleted:
                continue

            messages.append({
                'id': entry.message.id,
                'username': entry.message.user.username,
                'message_text': entry.message.message_text,
                'pub_date': entry.message.pub_date.isoformat(),
            })
    except ObjectDoesNotExist:
        pass

    return render(request, 'app/index.html', {'messages_json': json.dumps(messages), 'last_state': last_state})

@login_required
@require_POST
@transaction.atomic
def post_message(request):
    message_arg = request.POST.get('message')

    if not message_arg:
        return redirect('/')

    message = Message(user=request.user, message_text=message_arg)
    message.save()
    MessageHistory(message=message, is_addition=True).save()

    return JsonResponse({'id': message.id, 'pub_date': message.pub_date})

@login_required
@require_http_methods(['DELETE'])
@transaction.atomic
def delete_message(request, id):
    message_id = int(id)

    try:
        message = Message.objects.get(user=request.user, id=message_id)
        message.is_deleted = True
        message.save()
        MessageHistory(message=message, is_addition=False).save()
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    return HttpResponse(status=204)

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
