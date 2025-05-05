"""
Views for the main page
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models.captured_image_model import CapturedImage
from ..models.badge_model import Badge


@login_required
def home_view(request):
    context = {}

    captures = CapturedImage.objects.filter(user=request.user).order_by('-uploaded_at')
    all_captures = CapturedImage.objects.all().order_by('-uploaded_at')[:60]
    unlocked_badges = Badge.objects.filter(users=request.user).order_by('name') 

    context['captures'] = captures
    context['all_captures'] = all_captures
    context['unlocked_badges'] = unlocked_badges 

    return render(request, 'home/index.html', context)
