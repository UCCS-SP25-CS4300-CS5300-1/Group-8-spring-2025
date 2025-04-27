"""
Views for the friends system
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import FriendList, FriendRequest


@login_required
def friend_list(request):
    profile = request.user.profile
    f_list = FriendList.objects.get(profile=profile)
    friends = f_list.friends.all()
    requests = FriendRequest.objects.all()

    context = {'profile': profile, 'friend_list': f_list, 'friends': friends, 'requests': requests}
    return render(request, 'social/friend_list.html', context)
