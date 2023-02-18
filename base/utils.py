from base import models
from django.db.models import Q, Count


def update_home_context(context, request):
    q = request.GET.get('q', '')
    topics = models.Topic.objects.all() \
        .annotate(num_rooms=Count('room')) \
        .order_by('-num_rooms')[:3]
    room_messages = models.Message.objects.filter(
        Q(room__name__icontains=q) |
        Q(room__topic__name__icontains=q)
    )[:3]
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
