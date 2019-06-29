from django.db import models


class TradingSession(models.Model):
    roomId = models.IntegerField(default=0.0, null=False)
    startTime = models.CharField(max_length=255, null=False)
    endTime = models.CharField(max_length=255, null=False)
    endTimeCount = models.IntegerField(null=False)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.roomId, self.startTime, self.endTimeCount, self.userSelectedTraderId)
