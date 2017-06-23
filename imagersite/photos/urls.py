"""Routes for user user photos"""
from django.conf.urls import url
from photos.views import photos_view


urlpatterns = [
    url('^photos$', photos_view, name='photos')
]
