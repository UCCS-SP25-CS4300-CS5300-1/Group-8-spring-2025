import json
import os
import requests

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import IdentRequest


@receiver(post_save, sender=IdentRequest)
def identify(sender, instance, created, **kwargs):
    if instance.image and instance.req_status == IdentRequest.StatusChoices.CREATED:
        file = instance.image.file
        files = {
            'image': (instance.image.name, file),
        }

        data = {
            'req_id': instance.req_id,
        }

        response = requests.post(
            os.environ.get("IDENT_SERVER_HOST") + "/identify",
            files=files,
            data=data
        )

        # Handle response
        if response.status_code == 200:
            res_data = response.json()
            if res_data['status'] == 'received':
                instance.req_status = IdentRequest.StatusChoices.PENDING
            elif res_data['status'] == 'error':
                instance.req_status = IdentRequest.StatusChoices.FAILED
                instance.status_reason = res_data['message']

