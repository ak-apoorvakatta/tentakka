from django.db import models


class Users(models.Model):

    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    token = models.DecimalField(default=0.0, decimal_places=2, max_digits=13, null=False)

    def __str__(self):
        return "{} - {} - {}".format(self.username, self.password, self.token)
