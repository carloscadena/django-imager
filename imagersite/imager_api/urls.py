"""Urls for API."""
from django.conf.urls import url
from imager_api.views import profile_list

urlpatterns = [
    url(r'^profiles/$', profile_list, name='api'),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
