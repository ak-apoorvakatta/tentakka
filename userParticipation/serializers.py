from rest_framework import serializers
from .models import UserParticapation


class UserParticapationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserParticapation
        fields = ("userUsername", "traderId", "strategyId", "roomId", "investment")
