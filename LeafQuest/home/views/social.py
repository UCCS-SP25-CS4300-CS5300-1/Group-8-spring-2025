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
    captures = CapturedImage.objects.all()

    context = {'profile': profile, 'friends': friends, 'captures': captures}  
    return render(request, 'social/index.html', context)
