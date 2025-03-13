from django.shortcuts import render

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
    # TODO: perform logout action, then show LOGIN screen. No need for a logout template
    return render(request, 'logout/index.html')

def about_view(request):
    return render(request, 'about/index.html')