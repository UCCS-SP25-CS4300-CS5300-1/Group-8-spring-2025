from django.shortcuts import render, redirect
from home.models import Profile, FriendList, FriendRequest, CapturedImage, LeaderboardEntry
from django.contrib.auth.decorators import login_required
from ..forms import ProfileForm


@login_required
def profile_view(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    user_fl = FriendList.objects.get(profile=request.user.profile)
    leaderboard_entry = LeaderboardEntry.objects.get(profile=profile)
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

    context = {'profile': profile, 'sentReq': sentReq, 'is_friend': is_friend, 'leaderboard_entry': leaderboard_entry}

    # Get captured images
    captures = CapturedImage.objects.filter(user=profile.user)
    context['captures'] = captures

    return render(request, 'profile/index.html', context)


# redirects user to thier profile (for use with "Profile" button in the menu)
@login_required
def profile_redir(request):
    return(redirect('profile_view', request.user.profile.id))


# profile editing
@login_required
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
                  form.save()
    context = {'form': form}
    return render(request, 'profile/edit.html', context)
