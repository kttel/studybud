from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import User

from base import models


class ParticipantsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class RoomSerializer(ModelSerializer):
    participants = ParticipantsSerializer(many=True)

    class Meta:
        model = models.Room
        fields = ['name', 'description', 'host', 'participants']
