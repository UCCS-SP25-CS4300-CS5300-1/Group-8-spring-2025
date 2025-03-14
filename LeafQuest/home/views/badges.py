from django.shortcuts import render

def badges_view(request):
    return render(request, 'badges/index.html')
