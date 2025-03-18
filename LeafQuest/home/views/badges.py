from django.shortcuts import render
from ..models import Badge

def badges_view(request):
    all_badges = Badge.objects.all()
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_badges = request.user.badge_set.all()
    else:
        user_badges = None  # Handle anonymous users
    
    return render(request, 'badges/index.html', {'all_badges': all_badges, 'user_badges': user_badges})
