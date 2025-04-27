"""
Views for the PlantDex
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from ..models import Profile
from ..models.captured_image_model import CapturedImage


@login_required
def plantdex_view(request):
    context = {}

    captures = CapturedImage.objects.filter(user=request.user).order_by('-uploaded_at')
    context['captures'] = captures

    return render(request, 'plantdex/index.html', context)


@login_required
def plantdex_detail_view(request, pk):
    context = {}

    capture = get_object_or_404(CapturedImage, pk=pk)
    context['capture'] = capture

    context['user'] = capture.user
    context['profile'] = Profile.objects.get(user=capture.user)

    return render(request, 'plantdex/details.html', context)
    