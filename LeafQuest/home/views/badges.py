from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Badge

@login_required
def badges_view(request):
    all_badges = Badge.objects.all()
    user_badges = Badge.objects.filter(users=request.user).order_by('pk')
    
    return render(request, 'badges/index.html', {
        'all_badges': all_badges,
        'user_badges': user_badges
    })
