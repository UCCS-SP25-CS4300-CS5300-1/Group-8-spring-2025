from django.shortcuts import render
from ..models import Profile
from ..models import FriendList
from ..models import CapturedImage
from django.contrib.auth.decorators import login_required


@login_required
def social_view(request):
    profile = request.user.profile
    friend_list = FriendList.objects.get(profile=profile)
    friends = friend_list.friends.all()
    all_captures = CapturedImage.objects.all().order_by('-uploaded_at')

    context = {'profile': profile, 'friends': friends, 'all_captures': all_captures}  
    return render(request, 'social/index.html', context)
