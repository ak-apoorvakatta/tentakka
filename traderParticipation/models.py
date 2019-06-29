from django.db import models


class TraderParticapation(models.Model):
    roomId = models.IntegerField(default=0.0, null=False)
    traderId = models.CharField(max_length=255, null=False)
    traderName = models.CharField(default="Trader X", max_length=255, null=False)
    strategyId = models.CharField(max_length=255, null=False)
    mean = models.FloatField(default=0.0, null=False)
    std = models.FloatField(default=0.0, null=False)
    expectancy = models.FloatField(default=0.0, null=False)
    maxDD = models.FloatField(default=0.0, null=False)
    sharpe = models.FloatField(default=0.0, null=False)
    sortino = models.FloatField(default=0.0, null=False)
    predicted_return = models.FloatField(default=0.0, null=False)
    odds_of_win = models.FloatField(default=0.0, null=False)

    def __str__(self):
        return "{} - {} - {}".format(self.traderId, self.strategyId, self.roomId)
