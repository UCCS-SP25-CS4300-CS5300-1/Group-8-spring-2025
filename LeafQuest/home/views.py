from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.views import generic
from django.shortcuts import get_object_or_404

# Create your views here.
def home_view(request):
    return render(request, 'home/index.html')

def profile_view(request):
    return render(request, 'profile/index.html')

def capture_view(request):
    return render(request, 'capture/index.html')

def plantdex_view(request):
    return render(request, 'plantdex/index.html')

def badges_view(request):
    return render(request, 'badges/index.html')

def map_view(request):
    return render(request, 'map/index.html')

def social_view(request):
    return render(request, 'social/index.html')

def settings_view(request):
    return render(request, 'settings/index.html')

def logout_view(request):
    return render(request, 'logout/index.html')

def about_view(request):
    return render(request, 'about/index.html')

# user registration page
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            profile = Profile.objects.create(user=user,)
            profile.save()
            friendlist = FriendList.objects.create(profile=profile)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
       
    context = {'form': form}
    return render(request, 'registration/register.html', context)

# profile customization
def userPage(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)
    print('profile', profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
                  form.save()
    context = {'form': form}
    return render(request, 'profile/user.html', context)

# profile display for a given user
def profile_detail(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    sentReq = False

    # check if a pending friend request from the current user to this profile exists
    if FriendRequest.objects.filter(sender=request.user.profile, receiver=profile, pending=True).exists():
        sentReq = True

    context = {'profile': profile, 'sentReq': sentReq}
    return render(request, 'profile/profile_detail.html', context)

# create a friend request
def add_friend(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    req, created = FriendRequest.objects.get_or_create(sender=request.user.profile, receiver=profile)

    if created:
        messages.success(request, 'Sent a friend request to ' + profile.user.username)
    else: 
        messages.error(request, 'You already sent a friend request to this user')

    return(redirect('profile_detail', profile_id))

# cancel a friend request
def cancel_friend(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    req = FriendRequest.objects.get(sender=request.user.profile, receiver=profile)

    return(redirect('profile_detail', profile_id))

# accept friend request
def accept_req(request, request_id):
    req = FriendRequest.objects.get(pk=request_id)
    req.accept()

    messages.success(request, 'You are now friends with ' + req.sender.user.username)

    return(redirect('friend_list'))

# decline friend request
def decline_req(request, request_id):
    req = FriendRequest.objects.get(pk=request_id)
    req.decline()

    messages.success(request, 'You declined the request from ' + req.sender.user.username)

    return(redirect('friend_list'))


def friend_list(request):
    profile = request.user.profile
    friend_list = FriendList.objects.get(profile=profile)
    friends = friend_list.friends.all()
    requests = FriendRequest.objects.all()

    context = {'profile': profile, 'friend_list': friend_list, 'friends': friends, 'requests': requests}
    return render(request, 'profile/friend_list.html', context)

