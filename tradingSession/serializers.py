from rest_framework import serializers
from .models import *


class TradingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradingSession
        fields = ("id", "roomId", "startTime", "endTime", "endTimeCount")
