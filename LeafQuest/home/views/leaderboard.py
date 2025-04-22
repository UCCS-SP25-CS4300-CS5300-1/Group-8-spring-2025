from django.shortcuts import render
from ..models import Profile, FriendList, LeaderboardEntry
from django.contrib.auth.decorators import login_required

def leaderboard_view(request):
    profile = request.user.profile
    friend_list = FriendList.objects.get(profile=profile)
    friends = friend_list.friends.all()
    leaderboard_entries = LeaderboardEntry.objects.all().order_by('rank')

    context = {'profile': profile, 'friends': friends, 'leaderboard_entries': leaderboard_entries}
    return render(request, 'social/leaderboard.html', context)