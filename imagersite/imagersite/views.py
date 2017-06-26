"""Views for the home page."""
from django.shortcuts import render
from imager_images.models import Photo
import random
# from imagersite.settings import MEDIA_ROOT

def home_view(request):
    """View for home page."""
    images = Photo.objects.all().filter(published='PU')
    image_url = None
    if images:
        random_img = random.choice(images)
        image_url = random_img.image.url
    else:
        image_url = '/test/testing.png'

    context = {
        'stuff': 'somestuff',
        'rando_imag': image_url
    }
    return render(request, 'imagersite/home.html', context=context)
