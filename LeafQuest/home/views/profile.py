"""
Views for the profile
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import ProfileForm
from ..models.leaderboard_models import Leaderboard
from ..models.profile_model import Profile
from ..models.friend_models import FriendList, FriendRequest
from ..models.captured_image_model import CapturedImage
from ..models.badge_model import Badge


@login_required
def profile_view(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    user_fl = FriendList.objects.get(profile=request.user.profile)
    badges = Badge.objects.all()
    is_friend = False
    sent_req = False

    # check if current user and the profile's user are friends
    for friend in user_fl.friends.all():
        if friend == profile:
            is_friend = True
            break

    # check if a pending friend request from the current user to this profile exists
    if not is_friend:
        if FriendRequest.objects.filter(sender=request.user.profile, receiver=profile, pending=True).exists():
            sent_req = True

    context = {'profile': profile, 'sentReq': sent_req, 'is_friend': is_friend}

    # Get captured images
    captures = CapturedImage.objects.filter(user=profile.user).order_by('-uploaded_at')
    context['captures'] = captures
    context['badges'] = badges

    # Get the leaderboard entry for this user
    leaderboard_entry = None
    try:
        leaderboard_entry = Leaderboard.objects.get(profile=profile)
    except Leaderboard.DoesNotExist:
        leaderboard_entry = Leaderboard.objects.create(user=profile.user, profile=profile, num_captures=len(captures))
    context['leaderboard_entry'] = leaderboard_entry

    return render(request, 'profile/index.html', context)


# redirects user to thier profile (for use with "Profile" button in the menu)
@login_required
def profile_redir(request):
    return redirect('profile_view', request.user.profile.id)


# profile editing
@login_required
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'profile/edit.html', context)
