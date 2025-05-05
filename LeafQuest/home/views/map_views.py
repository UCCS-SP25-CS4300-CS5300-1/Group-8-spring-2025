"""
Views
"""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from identify_api.models import IdentRequest, StatusChoices
from ..models import MapPin, CapturedImage


@login_required
def map_view(request):
    return render(request, 'map/index.html')


@login_required
def get_user_pins(request):
    pins = MapPin.objects.filter(user=request.user)
    return JsonResponse([{
        'id': pin.id,
        'name': pin.name,
        'lat': pin.lat,
        'lng': pin.lng,
    } for pin in pins], safe=False)


@csrf_exempt
@require_POST
@login_required
def save_pin(request):
    data = json.loads(request.body)
    pin = MapPin.objects.create(
        user=request.user,
        name=data['name'],
        lat=data['lat'],
        lng=data['lng']
    )
    return JsonResponse({'id': pin.id})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def update_pin(request, pin_id):
    data = json.loads(request.body)
    pin = get_object_or_404(MapPin, id=pin_id, user=request.user)
    pin.name = data.get("name", pin.name)
    pin.save()
    return JsonResponse({'success': True, 'name': pin.name})


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def delete_pin(request, pin_id):
    pin = get_object_or_404(MapPin, id=pin_id, user=request.user)
    pin.delete()
    return JsonResponse({'success': True})

@login_required
def get_capture_pins(request):
    captures = IdentRequest.objects.filter(
        req_status=StatusChoices.RETURNED,
        gps_latitude__isnull=False,
        gps_longitude__isnull=False,
        result__isnull=False,
    )

    pin_list = []
    for capture in captures:
        lat = capture.gps_latitude
        lon = capture.gps_longitude
        name = capture.result

        capture_objects = CapturedImage.objects.filter(ident_request=capture)
        if len(capture_objects) < 0:
            continue  # skip this ident request if it's a dangling capture with no CapturedImage associated

        if capture.gps_lat_north is False:
            lat = -lat
        if capture.gps_lon_west is True:
            lon = -lon

        pin_list.append({
            'name': name,
            'lat': lat,
            'lng': lon,
            'image_url': capture.image.url,
            'user': capture_objects[0].user.username,
            'id': capture_objects[0].id,
        })

    return JsonResponse(pin_list, safe=False)
