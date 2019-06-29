from django.db import models


class UserParticapation(models.Model):

    userUsername = models.TextField(null=False)
    traderId = models.CharField(max_length=255, null=False)
    strategyId = models.CharField(default="", max_length=255, null=False)
    roomId = models.IntegerField(default=0.0, null=False)
    investment = models.DecimalField(default=0.0, decimal_places=2, max_digits=13, null=False)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.userUsername, self.traderId, self.roomId, self.investment)
