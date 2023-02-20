from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from rest_framework import generics, viewsets

from base import models
from base.api import serializers


class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
