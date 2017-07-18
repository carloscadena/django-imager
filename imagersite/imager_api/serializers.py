"""Module for serializing data."""
from django.contrib.auth.models import User
from imager_images.models import Album
from imager_images.models import Photo
from imager_profile.models import ImagerProfile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User."""

    class Meta(object):
        """Add options."""

        model = User
        fields = (
            'name', 'email', 'profile'
        )


class ImagerSerializer(serializers.ModelSerializer):
    """Serializer for profile."""

    class Meta(object):
        """Add options."""

        model = ImagerProfile
        fields = (
            'location', 'creation_date', 'LEVELS',
            'photog_level', 'website', 'headline'
        )


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for photo."""

    class Meta(object):
        """Add options."""

        model = Photo
        fields = (
            'title', 'description', 'profile', 'image', 'date_uploaded',
            'date_modified', 'date_published', 'published'
        )


class AlbumSerializer(serializers.ModelSerializer):
    """Serializer for album."""

    class Meta(object):
        """Add options."""

        model = Album
        fields = (
            'profile', 'title', 'description', 'date_uploaded',
            'date_modified', 'date_published', 'published',
            'cover_photo', 'photos'
        )
