from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from imager_api.serializers import ImagerSerializer
from imager_images.models import Album
from imager_images.models import Photo
from imager_profile.models import ImagerProfile


@csrf_exempt
def profile_list(request):
    """Profile Api View."""

    if request.method == 'GET':
        import pdb; pdb.set_trace()
        profile = ImagerProfile.objects.all()
        serializer = ImagerSerializer(ProfileTestCase, many=True)
        return JsonResponse(serializer.data, safe=False)
