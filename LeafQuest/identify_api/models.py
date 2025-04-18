import uuid

from django.db import models
from django.db.models import ImageField



# Create your models here.
class IdentRequest(models.Model):
    """An IdentRequest stores information about a request to identify a plant"""
    req_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class StatusChoices(models.IntegerChoices):
        CREATED = 1
        PENDING = 2
        RETURNED = 3
        FAILED = 4

    req_status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.CREATED)
    status_reason = models.TextField(null=True)

    image = ImageField(upload_to='captures/', null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    gps_latitude = models.FloatField(null=True, blank=True)
    gps_lat_north = models.BooleanField(null=True, blank=True)

    gps_longitude = models.FloatField(null=True, blank=True)
    gps_lon_west = models.BooleanField(null=True, blank=True)

    def __str__(self):
        if self.req_status == self.StatusChoices.CREATED:
            return f'CREATED - {self.req_id}'
        elif self.req_status == self.StatusChoices.PENDING:
            return f'PENDING - {self.req_id}'
        elif self.req_status == self.StatusChoices.RETURNED:
            return f'RETURNED - {self.req_id}'
        elif self.req_status == self.StatusChoices.FAILED:
            return f'FAILED - {self.req_id}'



