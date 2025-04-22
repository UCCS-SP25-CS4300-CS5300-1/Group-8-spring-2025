from django.shortcuts import render, redirect
from ..forms import CapturedImageForm
from ..models import LeaderboardEntry, LeaderboardManager
from django.contrib.auth.decorators import login_required


@login_required
def capture_view(request):
    if request.method == 'POST':
        form = CapturedImageForm(request.POST, request.FILES)
        if form.is_valid():
            captured_image = form.save(commit=False)
            captured_image.user = request.user
            captured_image.save()

            # update rankings following capture upload
            entry = LeaderboardEntry.objects.get(profile=request.user.profile)
            manager = LeaderboardManager.objects.get(pk=1)
            manager.update_rank(entry)
            
            return redirect('capture')
    else:
        form = CapturedImageForm()

    return render(request, 'capture/index.html', {'form': form})
