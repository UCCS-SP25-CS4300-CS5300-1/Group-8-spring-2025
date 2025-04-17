from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models.captured_image_model import CapturedImage

@login_required
def home_view(request):
    context = {}

    # Get captured images
    captures = CapturedImage.objects.filter(user=request.user)
    all_captures = CapturedImage.objects.all()
    context['captures'] = captures
    context['all_captures'] = all_captures

    return render(request, 'home/index.html', context)
