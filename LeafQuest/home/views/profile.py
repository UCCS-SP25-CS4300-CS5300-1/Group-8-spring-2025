from django.shortcuts import render, redirect
from home.models import Profile, FriendList, FriendRequest
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    user_fl = FriendList.objects.get(profile=request.user.profile)
    is_friend = False
    sentReq = False

    # check if current user and the profile's user are friends
    for friend in user_fl.friends.all():
        if friend == profile:
            is_friend = True
            break

    # check if a pending friend request from the current user to this profile exists
    if not is_friend:
        if FriendRequest.objects.filter(sender=request.user.profile, receiver=profile, pending=True).exists():
            sentReq = True

    context = {'profile': profile, 'sentReq': sentReq, 'is_friend': is_friend}
    return render(request, 'profile/index.html', context)


# redirects user to thier profile (for use with "Profile" button in the menu)
@login_required
def profile_redir(request):
    return(redirect('profile_view', request.user.profile.id))
