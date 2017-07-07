"""Routes for user public images."""
from django.conf.urls import url
from imager_images.views import library_view
from django.views.generic import ListView
from imager_images.models import Photo
from imager_images.models import Album
from imager_images.views import AlbumsView


urlpatterns = [
    url(r'^library/$', library_view, name='library'),
    url(r'^photos/$', ListView.as_view(
        template_name="imager_images/photos.html",
        model=Photo,
        context_object_name="photos",
        queryset=Photo.objects.filter(published="PU")

    ), name='photos'),
    url(r'^albums/$', ListView.as_view(
        template_name="imager_images/albums.html",
        model=Album,
        context_object_name="albums",
        queryset=Album.objects.filter(published="PU")
    ), name='albums'),
    url(r'^albums/(?P<album_id>\d+)$', AlbumsView.as_view(), name='album')
]
