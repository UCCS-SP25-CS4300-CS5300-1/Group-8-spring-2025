"""
Signals for plant identification requests
"""
import os
import requests
import piexif

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import IdentRequest


def _strip_gps_and_return(instance):
    image = instance.image.path
    exif = piexif.load(image)

    if "GPS" in exif and len(exif["GPS"]) > 0:
        try:
            # remove seconds from calculation to improve privacy
            # Precision should be between 4.5 and 11.1 km depending on latitude
            gps = exif["GPS"]
            lat_deg = gps[2][0][0] / gps[2][0][1]
            lat_min = gps[2][1][0] / gps[2][1][1]
            lat = lat_deg + (lat_min / 60)
            if gps[1].decode("utf-8") == "N":
                gps_lat_north = True
            elif gps[1].decode("utf-8") == "S":
                gps_lat_north = False

            lon_deg = gps[4][0][0] / gps[4][0][1]
            lon_min = gps[4][1][0] / gps[4][1][1]
            lon = lon_deg + (lon_min / 60)
            if gps[3].decode("utf-8") == "W":
                gps_lon_west = True
            elif gps[3].decode("utf-8") == "E":
                gps_lon_west = False

            if lat != instance.gps_latitude or lon != instance.gps_longitude:
                instance.gps_latitude = lat
                instance.gps_lat_north = gps_lat_north
                instance.gps_longitude = lon
                instance.gps_lon_west = gps_lon_west
                instance.save()

            # Ensure EXIF stripped from image
            try:
                exif["GPS"] = {}
                exif_bytes = piexif.dump(exif)
                piexif.insert(exif_bytes, image)
            except ValueError:
                print("Error Stripping Exif Data on IdentRequest", instance.req_id)
        # pylint: disable-next=broad-exception-caught
        except Exception as e:
            print("Error Processing GPS Data", instance.req_id, e, gps)


@receiver(post_save, sender=IdentRequest)
def identify(sender, instance, created, **kwargs):
    # Strip EXIF from image and save low-accuracy gps data
    if instance.image:
        _strip_gps_and_return(instance)

    # send identity request
    if instance.image and instance.req_status == IdentRequest.StatusChoices.CREATED:
        file = instance.image.file
        files = {
            'image': (instance.image.name, file),
        }

        data = {
            'req_id': instance.req_id,
        }

        try:
            response = requests.post(
                os.environ.get("IDENT_SERVER_HOST", 'http://localhost:8080') + "/identify",
                files=files,
                data=data,
                timeout=2
            )

            # Handle response
            if response.status_code == 200:
                res_data = response.json()
                if res_data['status'] == 'received':
                    instance.req_status = IdentRequest.StatusChoices.PENDING
                    instance.save()
                elif res_data['status'] == 'error':
                    instance.req_status = IdentRequest.StatusChoices.FAILED
                    instance.status_reason = res_data['message']
                    instance.save()

        # pylint: disable-next=broad-exception-caught
        except Exception as _e:
            instance.req_status = IdentRequest.StatusChoices.FAILED
            instance.status_reason = "Identity Server Unreachable"
            instance.save()
