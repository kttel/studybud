from base import models
from django.db.models import Q, Count


def post_message(room_id, request):
    room = models.Room.objects.get(pk=room_id)
    user = request.user
    message = models.Message.objects.create(
        user=user,
        room=room,
        body=request.POST.get('body'),
    )
    room.participants.add(user)
    return message


def update_profile_context(context):
    rooms = context['user'].room_set.all()
    room_messages = context['user'].message_set.all()
    topics = models.Topic.objects.all()[:3]

    context.update({
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    })
    return context


def update_home_context(context, request):
    q = request.GET.get('q', '')
    topics = models.Topic.objects.all() \
        .annotate(num_rooms=Count('room')) \
        .order_by('-num_rooms')[:3]
    room_messages = models.Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(room__topic__name__icontains=q)
    )
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    context.update({
        'topics': topics,
        'room_messages': room_messages,
        'rooms': rooms,
    })
    return context
