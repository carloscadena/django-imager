"""Urls for API."""
from django.conf.urls import url
from imager_api.views import photo_list

urlpatterns = [
    url(r'^photos/$', photo_list, name='api')
]
