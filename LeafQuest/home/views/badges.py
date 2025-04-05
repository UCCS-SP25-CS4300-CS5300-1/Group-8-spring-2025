from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Badge


@login_required
def badges_view(request):
    all_badges = Badge.objects.all()
    
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user_badges = Badge.objects.filter(user=request.user).order_by('pk')
    else:
        user_badges = None  # Handle anonymous users
    
    return render(request, 'badges/index.html', {'all_badges': all_badges, 'user_badges': user_badges})
