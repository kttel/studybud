from base import models


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
