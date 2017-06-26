from django.shortcuts import render
from imager_images.models import Album, Photo


def profile_view(request):
    albums = Album.objects.all()
    photos = Photo.objects.all()
    context = {'albums': albums, 'photos': photos}
    return render(request, 'imager_profile/profile.html', context=context)
