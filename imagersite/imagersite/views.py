"""Views for the home page."""
from django.shortcuts import render
from imager_images.models import Photo
import random


def home_view(request):
    """View for home page."""
    images = Photo.objects.filter(published='PU')
    if images:
        random_image = random.choice(images)
    else:
        random_image = None

    context = {
        'stuff': 'somestuff',
        'random_image': random_image
    }
    return render(request, 'imagersite/home.html', context=context)
