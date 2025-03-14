from django.shortcuts import render

def social_view(request):
    return render(request, 'social/index.html')
