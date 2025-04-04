from django.shortcuts import render
from ..models import Profile

def profile_search(request):
    if request.method == "POST":
        search = request.POST['search']
        results = Profile.objects.filter(user__username__contains = search)
        return render(request, 'social/profile_search.html', {'search': search, 'results': results})
    return render(request, 'social/profile_search.html')