from django.shortcuts import render

def capture_view(request):
    return render(request, 'capture/index.html')
