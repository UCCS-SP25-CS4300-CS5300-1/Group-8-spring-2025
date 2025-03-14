from django.shortcuts import render

def plantdex_view(request):
    return render(request, 'plantdex/index.html')
    