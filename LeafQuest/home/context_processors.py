"""
Functions to add variables to the context for every view
"""
from .models import ClientPreferences


def client_preferences(request):
    context = {}
    if hasattr(request, 'user'):
        if request.user.is_authenticated:
            preferences = ClientPreferences.objects.get_or_create(user=request.user)[0]
            context["USE_DARK_MODE"] = preferences.use_dark_mode
    return context
