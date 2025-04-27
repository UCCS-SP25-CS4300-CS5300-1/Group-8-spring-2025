"""
Views to handle friend request management
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Profile, FriendList, FriendRequest


# create a friend request
@login_required
def add_friend(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    _req, created = FriendRequest.objects.get_or_create(sender=request.user.profile, receiver=profile, pending=True)

    if profile != request.user.profile:
        if created:
            messages.success(request, 'Sent a friend request to ' + profile.user.username)
        else:
            messages.error(request, 'You already sent a friend request to this user')

    return redirect('profile_view', profile_id)


# cancel a friend request
def cancel_friend(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    req = FriendRequest.objects.get(sender=request.user.profile, receiver=profile, pending=True)

    req.cancel()

    return redirect('profile_view', profile_id)


# remove an existing friend
def remove_friend(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    profile_friends = FriendList.objects.get(profile=profile)
    user_friends = FriendList.objects.get(profile=request.user.profile)

    profile_friends.remove_friend(request.user.profile)
    user_friends.remove_friend(profile)

    return redirect('profile_view', profile_id)


# accept friend request
def accept_req(request, request_id):
    req = FriendRequest.objects.get(pk=request_id)
    req.accept()

    messages.success(request, 'You are now friends with ' + req.sender.user.username)

    return redirect('friend_list')


# decline friend request
def decline_req(request, request_id):
    req = FriendRequest.objects.get(pk=request_id)
    req.decline()

    messages.success(request, 'You declined the request from ' + req.sender.user.username)

    return redirect('friend_list')
