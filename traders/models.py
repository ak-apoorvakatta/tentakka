from django.db import models


class Traders(models.Model):

    traderid = models.CharField(max_length=255, null=False)
    dateindex = models.IntegerField(null=False)
    value = models.FloatField(null=False)
    strategyid = models.CharField(max_length=255, null=False)


    def __str__(self):
        return "{} - {} - {} - {}".format(self.traderid, self.dateindex, self.value, self.strategyid)
