"""Routes for user public images."""
from django.conf.urls import url
from imager_images.views import LibraryView
from imager_images.views import AlbumsView
from imager_images.views import AlbumView
from imager_images.views import AlbumAdd
from imager_images.views import PhotoAdd
from imager_images.views import PhotoEdit
from imager_images.views import AlbumEdit, PhotosView

urlpatterns = [
    url(
        r'^library/(?P<album_page_num>\d*)/(?P<photo_page_num>\d*)$',
        LibraryView.as_view(),
        name='library'
    ),
    url(r'^photos/page/(?P<page_num>\d*)$', PhotosView.as_view(), name='photos'),
    url(r'^albums/page/(?P<page_num>\d*)$', AlbumsView.as_view(), name='albums'),
    url(
        r'^album/(?P<album_id>\d+)/(?P<page_num>\d*)$',
        AlbumView.as_view(),
        name='album'
    ),
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
