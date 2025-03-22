from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def badges_view(request):
    return render(request, 'badges/index.html')
