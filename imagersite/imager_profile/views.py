from django.shortcuts import render
from imager_images.models import Album, Photo


def profile_view(request):
    albums = Album.objects.all()
    # import pdb; pdb.set_trace()
    photos = Photo.objects.all()
    context = {'albums': albums, 'photos': photos}
    return render(request, 'imager_profile/profile.html', context=context)
