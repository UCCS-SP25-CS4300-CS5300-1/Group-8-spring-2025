from django.shortcuts import render, redirect
from ..forms import CreateUserForm
from django.contrib import messages
from ..models import Profile, FriendList, Leaderboard
from django.contrib.auth import login

# user registration page
def register_view(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            profile = Profile.objects.create(user=user)
            profile.save()
            friendlist = FriendList.objects.create(profile=profile)
            leaderboardentry = Leaderboard.objects.create(profile=profile, user=profile.user)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
       
    context = {'form': form}
    return render(request, 'registration/register.html', context)
