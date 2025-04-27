"""
Views for log out (Consider merging with login and account creation for an auth view file)
"""
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged Out!')
    return redirect('login')
