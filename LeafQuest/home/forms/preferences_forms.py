"""
Forms for user settings and preferences
"""

from django import forms

from ..models import ClientPreferences


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = ClientPreferences
        fields = ['use_dark_mode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})