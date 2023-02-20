from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model

from base import models


class ParticipantsSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class RoomSerializer(ModelSerializer):
    participants = ParticipantsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Room
        fields = ['id', 'name', 'description', 'host', 'participants']
        read_only_fields = ['host']

    def create(self, validated_data):
        room = models.Room.objects.create(**validated_data)
        room.host = self.context.get('request').user
        room.save()
        return room

class UserSerializer(ModelSerializer):
    room_set = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'bio', 'room_set']
        read_only_fields = ['id', 'email']