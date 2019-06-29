from django.db import models


class Rooms(models.Model):

    roomName = models.CharField(max_length=255, null=False)
    status = models.IntegerField(default=0, null=False)
    active = models.IntegerField(default=0, null=False)
    createdAt = models.DateField(null=False)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.roomName, self.status, self.active, self.createdAt)
