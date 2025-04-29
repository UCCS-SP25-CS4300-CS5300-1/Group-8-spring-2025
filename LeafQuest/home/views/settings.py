"""
Views for user settings
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    if request.method == "POST":
        preferences = ClientPreferences.objects.filter(user=request.user)[0]
        form = PreferencesForm(request.POST)
        if form.is_valid():
            use_dark_mode = form.cleaned_data['use_dark_mode']
            preferences.use_dark_mode = use_dark_mode
            preferences.save()

            context['form'] = form
            messages.success(request, 'Settings Saved')

            return render(request, 'settings/index.html', context)
        else:
            context['form'] = form
            messages.error(request, 'Error saving settings\n' + form.errors)
            return render(request, 'settings/index.html', context)
