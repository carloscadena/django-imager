from django.shortcuts import render
from imager_images.models import Album, Photo
from django.contrib.auth.models import User


def profile_view(request, **kwargs):
    # import pdb; pdb.set_trace()
    # if kwargs['username']is None:
    username = kwargs['username']
    the_user = User.objects.get(username=username)
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
