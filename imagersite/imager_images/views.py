"""Views for displaying images and albums."""
from django.shortcuts import render
from imager_images.models import Photo
from imager_images.models import Album
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


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


def albums_view(request, album_id=None):
    """View for the publicly uploaded albums."""
    if not album_id:
        albums = Album.objects.all().filter(published='PU')

        context = {
            'albums': albums,
        }
        return render(request, 'imager_images/albums.html', context=context)
    try:
        the_album = Album.objects.get(id=album_id, published="PU")
    except ObjectDoesNotExist:
        return redirect('albums')
    # import pdb; pdb.set_trace()
    context = {
        'album': the_album,
        'photos': the_album.photos.all()
    }
    return render(request, 'imager_images/photos.html', context=context)
