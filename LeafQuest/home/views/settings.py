"""
Views for user settings
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import ClientPreferences
from ..forms.preferences_forms import PreferencesForm

@login_required
def settings_view(request):
    context = {}

    if request.method == "GET":
        preferences = ClientPreferences.objects.filter(user=request.user)[0]
        form = PreferencesForm(instance=preferences)
        context['form'] = form
        return render(request, 'settings/index.html', context)
