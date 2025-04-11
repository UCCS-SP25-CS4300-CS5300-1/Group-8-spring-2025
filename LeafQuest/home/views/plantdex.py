from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Profile
from ..models.captured_image_model import CapturedImage


@login_required
def plantdex_view(request):
    context = {}

    captures = CapturedImage.objects.filter(user=request.user)
    context['captures'] = captures

    return render(request, 'plantdex/index.html', context)

@login_required
def plantdex_detail_view(request, pk):
    context = {}

    capture = CapturedImage.objects.get(pk=pk)
    context['capture'] = capture

    context['user'] = capture.user
    context['profile'] = Profile.objects.get(user=capture.user)

    return render(request, 'plantdex/details.html', context)
    