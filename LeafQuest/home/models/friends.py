from django.db import models
from .profile import Profile

# friend list for a given user
class FriendList(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    friends = models.ManyToManyField(Profile, blank=True, related_name='friends')
 
    # add a friend
    def add_friend(self, friend):
        # add friend if friend isn't already added
        if not friend in self.friends.all():
            self.friends.add(friend)

    # remove a friend
    def remove_friend(self, friend):
        # remove friend if friend is added
        if friend in self.friends.all():
            self.friends.remove(friend)

# friend request from one user to another
class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')

    pending = models.BooleanField(blank=True, default=True)

    # more readable name for model
    def __str__(self):
        return self.sender.name + ' -> ' + self.reveiver.name
    
    # accept a friend request
    def accept(self):
        sender_friends = FriendList.objects.get(profile=self.sender)
        receiver_friends = FriendList.objects.get(profile=self.receiver)

        # check that both friend lists exist
        if sender_friends and receiver_friends:
            sender_friends.add_friend(self.receiver)
            receiver_friends.add_friend(self.sender)

        # request is no longer pending
        self.pending = False
        self.save()

    # decline friend request (receiver side)
    def decline(self):
        # set pending field to false to denote that request is declined
        self.pending = False
        self.save()

    # cancel friend request (sender side)
    def cancel(self):
        # set pending field to false to denote that request is cancelled
        self.pending = False
        self.save()