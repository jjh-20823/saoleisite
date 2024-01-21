from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Player(models.Model):
    name = models.CharField(max_length=20) # TODO Add a realname validator here
    pid = models.IntegerField(unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="player"
    )
    is_banned = models.BooleanField(
        default=False
    )  # Permission to videos

    @property
    def is_bound(self):
        return not self.user is None

    def __str__(self):
        return "{}[{}]".format(self.name, self.pid)

    def get_absolute_url(self):
        return reverse("player:player_zone", kwargs={"pid": self.pid})
