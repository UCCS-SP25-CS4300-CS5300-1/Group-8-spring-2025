from django.db import models
from .profile_model import Profile

class LeaderboardEntry(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rank = models.IntegerField(default=Profile.objects.count())
    num_captures = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.name

class LeaderboardManager(models.Model):
    leaderboard_id = models.IntegerField()
    most_captures = models.IntegerField(default=0)

    # update the most_captures 
    def update_most_captures(self, entry):
        self.most_captures = entry.num_captures
        self.save()

    # shift ranks
    def shift_ranks(self, start_rank, direction):
        # get the QuerySet for all entries at or below the provided rank
        entries = LeaderboardEntry.objects.filter(rank__gte=start_rank)

        if direction == 0:
            # lower ranks for all users in QuerySet
            for entry in entries:
                entry.rank += 1
                entry.save()
        else:
            # raise ranks for all users in QuerySet
            for entry in entries:
                entry.rank -= 1
                entry.save()

    # to be called when a new capture is uploaded
    def update_rank(self, entry):
        # increment capture count
        entry.num_captures += 1

        # if user is #1 rank, update most_captures
        if entry.rank == 1:
            self.update_most_captures(entry)

        # user ties #1 captures
        elif entry.num_captures == self.most_captures:
            entry.rank = 1
            entry.save()
            entries = LeaderboardEntry.objects.filter(rank__gt=1)
            self.shift_ranks(2, 1)

        # user passes current #1
        elif entry.num_captures > self.most_captures:
            # drop previous #1 user(s) to #2
            entries = LeaderboardEntry.objects.filter(rank=1)
            for old_rank_1 in entries:
                old_rank_1.rank += 1
                old_rank_1.save()

            entry.rank = 1
            entry.save()
            self.update_most_captures(entry)
        
        # increase in num_captures has no bearing on #1 rank
        else:
            next_rank = entry.rank - 1
            entries = LeaderboardEntry.objects.filter(rank=next_rank)
            self.shift_ranks(next_rank, 0)

            entry.rank -= 1
            entry.save()



            


                
        
