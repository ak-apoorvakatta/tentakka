from rest_framework import serializers
from .models import TraderParticapation


class TraderParticapationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraderParticapation
        fields = ("id", "traderId", "strategyId", "roomId",
                  "mean", "std", "expectancy", "maxDD", "sharpe",
                  "sortino", "predicted_return", "odds_of_win", "traderName")
