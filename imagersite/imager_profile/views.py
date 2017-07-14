from django.shortcuts import render
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


def profile_view(request, username=None):
    """Create Profile View."""
    if not username:
        username = request.user.username
        if not username:
            return redirect('home')
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('home')

    profile = user.profile

    photos = Photo.objects.filter(profile=user.profile)

    albums = Album.objects.filter(profile=user.profile)

    data = {
        'photo_published': photos.filter(published="PUBLIC").count(),
        'photo_private': photos.filter(published="PRIVATE").count(),
        'album_published': albums.filter(published="PUBLIC").count(),
        'album_private': albums.filter(published="PRIVATE").count()
    }
    context = {'profile': profile, 'data': data}

    return render(request, 'imager_profile/profile.html', context=context)
