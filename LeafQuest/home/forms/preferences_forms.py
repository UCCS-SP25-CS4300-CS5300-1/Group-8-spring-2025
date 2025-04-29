"""
Forms for user settings and preferences
"""

from django import forms

from ..models import ClientPreferences


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = ClientPreferences
        fields = ['use_dark_mode']
