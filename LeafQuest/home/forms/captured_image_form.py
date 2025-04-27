"""
Form for receiving captured images
"""
from django import forms
from LeafQuest.identify_api.models import IdentRequest
from ..models import CapturedImage


class CapturedImageForm(forms.Form):
    image = forms.ImageField()

    def save(self, commit=True):
        image = self.cleaned_data['image']
        ident_request = IdentRequest.objects.create()

        # File name processing
        name = image.name
        ext = name.rsplit('.', 1)[1]
        if ext not in ['jpg', 'jpeg', 'png']:
            self.add_error('image', 'upload must be an image file')
            raise forms.ValidationError

        image.name = str(ident_request.req_id) + '.' + ext

        # Add image to object
        ident_request.image = image
        ident_request.save()

        captured_image = CapturedImage(ident_request=ident_request)
        if commit:
            captured_image.save()
        return captured_image
