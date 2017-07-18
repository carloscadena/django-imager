"""Routes for user public images."""
from django.conf.urls import url
from imager_images.views import LibraryView
from django.views.generic import ListView
from imager_images.models import Album
from imager_images.views import AlbumsView
from imager_images.views import AlbumAdd
from imager_images.views import PhotoAdd
from imager_images.views import PhotoEdit
from imager_images.views import AlbumEdit, PhotosView

urlpatterns = [
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^photos/$', PhotosView.as_view(), name='photos'),
    url(r'^albums/$', ListView.as_view(
        template_name="imager_images/albums.html",
        model=Album,
        context_object_name="albums",
        queryset=Album.objects.filter(published="PU")
    ), name='albums'),
    url(r'^albums/(?P<album_id>\d+)$', AlbumsView.as_view(), name='album'),
    url(r'^photos/add/$', PhotoAdd.as_view(), name='photo_add'),
    url(r'^albums/add/$', AlbumAdd.as_view(), name='album_add'),
    url(
        r'^photos/(?P<photo_id>\d+)/edit/$',
        PhotoEdit.as_view(),
        name='photo_edit'
    ),
    url(
        r'^albums/(?P<album_id>\d+)/edit/$',
        AlbumEdit.as_view(),
        name='album_edit'
    ),
    url(r'^tagged/(?P<slug>\w+)$', PhotosView.as_view(), name='tagged_photos')
]
