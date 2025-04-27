"""
Models for Leaderboard.
"""
from django.contrib.auth import get_user_model
from django.db import models
from .profile_model import Profile

User = get_user_model()


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    num_captures = models.IntegerField(default=0)
    rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Leaderboard Entry"
