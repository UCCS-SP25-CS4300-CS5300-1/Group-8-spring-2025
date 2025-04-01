from django.shortcuts import render
from ..forms import ProfileForm
from django.contrib.auth.decorators import login_required

# profile editing
@login_required
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
                  form.save()
    context = {'form': form}
    return render(request, 'profile/edit.html', context)