from django.shortcuts import render, redirect
from ..forms import CapturedImageForm
from ..models import Leaderboard
from django.contrib.auth.decorators import login_required


@login_required
def capture_view(request):
    if request.method == 'POST':
        form = CapturedImageForm(request.POST, request.FILES)
        if form.is_valid():
            captured_image = form.save(commit=False)
            captured_image.user = request.user
            captured_image.save()
            
            return redirect('capture')
    else:
        form = CapturedImageForm()

    return render(request, 'capture/index.html', {'form': form})
