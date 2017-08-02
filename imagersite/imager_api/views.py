"""View for photo api."""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from imager_api.serializers import PhotoSerializer
from imager_images.models import Photo


@csrf_exempt
def photo_list(request):
    """Photo Api View."""
    if request.method == 'GET':
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return JsonResponse(serializer.data, safe=False)
