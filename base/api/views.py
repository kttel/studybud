from rest_framework.response import Response
from rest_framework.decorators import api_view

from base import models
from base.api import serializers


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def get_rooms(request):
    rooms = models.Room.objects.all()
    serializer = serializers.RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, pk):
    room = models.Room.objects.get(pk=pk)
    serializer = serializers.RoomSerializer(room)
    return Response(serializer.data)
