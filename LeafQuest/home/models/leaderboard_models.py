from django.contrib.auth.models import User
from django.db import models
from .profile_model import Profile


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    num_captures = models.IntegerField(default=0)
    rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}'s Leaderboard Entry".format(self.user.username)
