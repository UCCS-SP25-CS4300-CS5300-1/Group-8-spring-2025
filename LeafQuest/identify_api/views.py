"""
Views for identify_api
"""
import json
import os
import uuid

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import IdentRequest


@csrf_exempt
def make_request(request):
    if request.method == "POST":
        if request.FILES.get('file', False):
            file = request.FILES['file']

            req = IdentRequest.objects.create()

            # File name processing
            name = file.name
            ext = name.rsplit('.', 1)[1]
            if ext not in ['jpg', 'jpeg', 'png']:
                return JsonResponse({'error': 'Invalid File Type'}, status=400)

            file.name = str(req.req_id) + '.' + ext

            # Add image to object
            req.image = file
            req.save()

            return JsonResponse({'ok': True})

        return JsonResponse({'error': 'No file provided'}, status=400)

    return JsonResponse({'error': 'Method Not Allowed'}, status=405)


@csrf_exempt
def return_ident(request):
    if request.method == "POST":
        response = json.loads(request.body)
        if response.get('req_id', False):
            req_id = response['req_id']
            request = IdentRequest.objects.get(req_id=uuid.UUID(req_id))

            prediction = response.get('prediction')
            confidence = float(response.get('confidence'))
            if confidence >= float(os.environ.get('CONFIDENCE_THRESHOLD', 0)):
                request.result = prediction
                request.confidence = confidence
                request.req_status = IdentRequest.StatusChoices.RETURNED
            else:
                request.req_status = IdentRequest.StatusChoices.FAILED
                request.status_reason = "No Plant Identified"

            request.save()
            return JsonResponse({'status': 'ok'})

        return JsonResponse({'error': 'No id provided'}, status=400)

    return JsonResponse({'error': 'Method Not Allowed'}, status=405)
