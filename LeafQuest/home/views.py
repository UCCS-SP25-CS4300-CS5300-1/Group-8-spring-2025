from django.shortcuts import render
from .forms import *
from django.contrib import messages

# Create your views here.
def home_view(request):
    return render(request, 'home/index.html')

def profile_view(request):
    return render(request, 'profile/index.html')

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
