from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def capture_view(request):
    return render(request, 'capture/index.html')
