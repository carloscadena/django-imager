"""Module for serializing data."""
from imager_images.models import Photo
from rest_framework import serializers


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for photo."""

    class Meta(object):
        """Add options."""

        model = Photo
        fields = (
            'title', 'description', 'profile', 'image', 'date_uploaded',
            'date_modified', 'date_published', 'published'
        )
