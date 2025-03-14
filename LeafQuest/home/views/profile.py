from django.shortcuts import render
from home.models import Profile, FriendRequest
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    sentReq = False

    # check if a pending friend request from the current user to this profile exists
    if FriendRequest.objects.filter(sender=request.user.profile, receiver=profile, pending=True).exists():
        sentReq = True

    context = {'profile': profile, 'sentReq': sentReq}
    return render(request, 'profile/index.html', context)
