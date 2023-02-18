from base import models


def update_profile_context(context):
    rooms = context['user'].room_set.all()
    room_messages = context['user'].message_set.all()[:3]
    topics = models.Topic.objects.all()[:3]

    context.update({
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,
    })
    return context
