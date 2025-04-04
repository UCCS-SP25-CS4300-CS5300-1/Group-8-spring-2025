from django.shortcuts import render
from ..models import Profile

# base view
def profile_search_view(request):
    return render(request, 'social/profile_search.html')

# view when search query is sent
def profile_search(request):
    if request.method == "GET":
        search = request.GET.get('search')
        results = Profile.objects.filter(user__username__contains = search)
        return render(request, 'social/profile_search.html', {'search': search, 'results': results})