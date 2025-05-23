"""
Views for the leaderboard
"""
from django.shortcuts import render
from ..models.friend_models import FriendList
from ..models.leaderboard_models import Leaderboard


def leaderboard_view(request):
    profile = request.user.profile
    friend_list = FriendList.objects.get(profile=profile)
    friends = friend_list.friends.all()
    leaderboard_entries = Leaderboard.objects.all().order_by('rank')

    context = {'profile': profile, 'friends': friends, 'leaderboard_entries': leaderboard_entries}
    return render(request, 'social/leaderboard.html', context)
