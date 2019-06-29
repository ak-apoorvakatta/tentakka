from rest_framework import serializers
from .models import *


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ("id", "roomName", "status", "active", "createdAt")
