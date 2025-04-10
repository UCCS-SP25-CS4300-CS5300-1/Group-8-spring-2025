
from django import forms
from ..models import CapturedImage
from identify_api.models import IdentRequest

class CapturedImageForm(forms.Form):
    image = forms.ImageField()

    def save(self, commit=True):
        image = self.cleaned_data['image']
        ident_request = IdentRequest.objects.create()

        # File name processing
        name = image.name
        ext = name.rsplit('.', 1)[1]
        if ext not in ['jpg', 'jpeg', 'png']:
            self.add_error('image', f'upload must be an image file')

        image.name = str(ident_request.req_id) + '.' + ext

        # Add image to object
        ident_request.image = image
        ident_request.save()

        captured_image = CapturedImage(ident_request=ident_request)
        if commit:
            captured_image.save()
        return captured_image

