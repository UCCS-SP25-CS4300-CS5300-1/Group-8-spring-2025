from django.shortcuts import render

def logout_view(request):
    # TODO: perform logout action, then show LOGIN screen. No need for a logout template
    return render(request, 'logout/index.html')
