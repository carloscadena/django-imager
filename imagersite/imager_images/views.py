"""Views for displaying images and albums."""
from django.shortcuts import render
from imager_images.models import Photo
from imager_images.models import Album


def library_view(request):
    """View for library page."""

    return render(request, 'imager_images/library.html')


def photos_view(request):
    """View for the publicly uploaded photos."""
    photos = Photo.objects.all().filter(published='PU')

    context = {
        'photos': photos
    }
    return render(request, 'imager_images/photos.html', context=context)


def albums_view(request):
    """View for the publicly uploaded albums."""
    albums = Album.objects.all().filter(published='PU')

    context = {
        'albums': albums,
    }
    return render(request, 'imager_images/albums.html', context=context)
