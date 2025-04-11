from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models.captured_image_model import CapturedImage


@login_required
def plantdex_view(request):
    context = {}

    captures = CapturedImage.objects.filter(user=request.user)
    context['captures'] = captures

    return render(request, 'plantdex/index.html', context)
    