from rest_framework import serializers
from .models import Traders


class TradersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traders
        fields = ("traderid", "dateindex", "value", "strategyid")
