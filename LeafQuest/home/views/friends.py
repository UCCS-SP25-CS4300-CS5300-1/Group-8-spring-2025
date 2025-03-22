from django.shortcuts import render
from ..models import FriendList, FriendRequest
from django.contrib.auth.decorators import login_required


@login_required
def friend_list(request):
    profile = request.user.profile
    friend_list = FriendList.objects.get(profile=profile)
    friends = friend_list.friends.all()
    requests = FriendRequest.objects.all()

    context = {'profile': profile, 'friend_list': friend_list, 'friends': friends, 'requests': requests}
    return render(request, 'profile/friend_list.html', context)
