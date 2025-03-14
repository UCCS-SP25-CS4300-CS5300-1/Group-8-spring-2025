from django.shortcuts import render
from home.forms import ProfileForm

# profile editing
def edit_profile(request):
    profile = request.user.profile
    form = ProfileForm(instance = profile)
    print('profile', profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
                  form.save()
    context = {'form': form}
    return render(request, 'profile/edit.html', context)