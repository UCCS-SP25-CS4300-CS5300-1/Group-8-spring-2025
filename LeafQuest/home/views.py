from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.views import generic

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

                  messages.success(request, 'Account was created for ' + username)
                  return redirect('login')
       
      context = {'form': form}
      return render(request, 'registration/register.html', context)

def userPage(request):
       profile = request.user.profile
       form = ProfileForm(instance = profile)
       print('profile', profile)

       if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                  form.save()
       context = {'form': form}
       return render(request, 'user.html', context)

class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
