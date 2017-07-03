"""Routes for user public images."""
from django.conf.urls import url
from imager_images.views import library_view
from imager_images.views import photos_view
from imager_images.views import albums_view


urlpatterns = [
    url(r'^library/$', library_view, name='library'),
    url(r'^photos/$', photos_view, name='photos'),
    url(r'^albums/$', albums_view, name='albums')
]
