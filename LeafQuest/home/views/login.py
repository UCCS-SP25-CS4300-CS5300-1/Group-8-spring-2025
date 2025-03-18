from django.shortcuts import render, redirect
from ..forms import LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user:
                login(request, user)
                messages.success(request, 'Hello, ' + request.user.username)
                return redirect('home')

    context = {'form': form}
    return render(request, 'registration/login.html', context)