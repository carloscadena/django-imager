from django.shortcuts import render
from imager_images.models import Album, Photo
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


def profile_view(request, username=None):
    if not username:
        username = request.user.username
        if not username:
            return redirect('home')
    try:
        the_user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect('home')

    profile = the_user.profile

    photo_data = Photo.objects.filter(profile=the_user.profile)

    album_data = Album.objects.filter(profile=the_user.profile)

    data = {
        'photo_published': photo_data.filter(published="PUBLIC").count(),
        'photo_private': photo_data.filter(published="PRIVATE").count(),
        'album_published': album_data.filter(published="PUBLIC").count(),
        'album_private': album_data.filter(published="PRIVATE").count()
    }
    context = {'profile': profile, 'data': data}

    return render(request, 'imager_profile/profile.html', context=context)
