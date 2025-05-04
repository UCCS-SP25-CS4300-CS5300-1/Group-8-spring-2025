"""
Views for the main page
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models.captures import CapturedImage
from ..models.badge_model import Badge


@login_required
def home_view(request):
    context = {}

    # Get captured images
    captures = CapturedImage.objects.filter(user=request.user).order_by('-uploaded_at')
    all_captures = CapturedImage.objects.all().order_by('-uploaded_at')

    # badges
    badges = Badge.objects.all()

    context['captures'] = captures
    context['all_captures'] = all_captures
    context['badges'] = badges

    return render(request, 'home/index.html', context)
