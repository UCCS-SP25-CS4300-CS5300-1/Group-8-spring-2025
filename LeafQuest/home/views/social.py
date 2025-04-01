from django.shortcuts import render
from ..models import Profile

def social_view(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    
    return render(request, 'social/index.html', context)
