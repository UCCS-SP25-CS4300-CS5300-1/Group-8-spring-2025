from django.db import models
from .profile_model import Profile


# leaderboard entry for a given user
# contains rank and number of captures
class LeaderboardEntry(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    rank = models.IntegerField(default=999999)
    num_captures = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.user.username


# methods to manage users on the leaderboard
class LeaderboardManager(models.Model):
    most_captures = models.IntegerField(default=0)
    starting_rank = models.IntegerField(default=0)

    # update the most_captures variable
    def update_most_captures(self, entry):
        self.most_captures = entry.num_captures
        self.save()

    # shift ranks up or down
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
            # for when a sole user at a given rank ties the next rank
            for entry in entries:
                entry.rank -= 1
                entry.save()

    # rank users after their first capture upload
    def first_capture(self, entry):
        entries = LeaderboardEntry.objects.filter(num_captures=1)
        
        # start user tied with other users that have 1 capture
        if entries:
            entry.rank = self.starting_rank

        # if no users have 1 capture, set user to the next lowest rank
        # update starting_rank accordingly
        else: 
            self.starting_rank = self.starting_rank + 1
            self.save()
            entry.rank = self.starting_rank

        entry.save()

    # to be called when a new capture is uploaded
    def update_rank(self, entry):
        # increment capture count
        entry.num_captures += 1

        # user increases capture count as current #1
        if entry.num_captures > self.most_captures:
            # drop previous #1 user(s) to #2
            self.shift_ranks(1, 0)
            entry.rank = 1
            entry.save()
            self.update_most_captures(entry)
        
        # increase in num_captures has no bearing on #1 rank
        else:
            # for users on the leaderboard
            if entry.num_captures > 1:
                current_rank = entry.rank
                next_rank = entry.rank - 1
                nr_entries = LeaderboardEntry.objects.filter(rank=next_rank)
                cr_entries = LeaderboardEntry.objects.filter(rank=current_rank)

                # capture count ties capture count of next ranked user
                if entry.num_captures == nr_entries[0].num_captures:
                    entry.rank -= 1
                    entry.save()

                    # if only user at current rank, shift ranks up
                    if not cr_entries:
                        self.shift_ranks(current_rank, 1)

                # capture count doesn't reach next rank
                else:
                    # if tied with other users, shift other users down
                    if cr_entries.count() > 1:
                        self.shift_ranks(entry.rank, 0)
                        entry.rank -= 1
                    entry.save()     

            # for users uploading their first capture
            else:
                self.first_capture(entry)
