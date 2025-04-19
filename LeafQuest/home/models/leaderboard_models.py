from django.db import models
from .profile_model import Profile

class LeaderboardEntry(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rank = models.IntegerField(default=Profile.objects.count())
    num_captures = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.name

class Leaderboard(models.Model):
    entries = models.ManyToManyField(LeaderboardEntry, blank=True, related_name='entries')