"""Image Models."""
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from imager_profile.models import ImagerProfile
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager


PUB_STATUS = (
    ('PR', 'Private'),
    ('SH', 'Shared'),
    ('PU', 'Public')
)


@python_2_unicode_compatible
class Photo(models.Model):
    """Photo Model."""

    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    profile = models.ForeignKey(ImagerProfile,
                                on_delete=models.CASCADE,
                                related_name="photos")
    image = ImageField(upload_to='photos')
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)

    published = models.CharField(
        max_length=2,
        choices=PUB_STATUS,
        default='PU'
    )
    tags = TaggableManager()

    def __repr__(self):
        """Show Photo."""
        return "<Photo: {}>".format(self.title)

    def __str__(self):
        """Show string."""
        return """
Photo: {}
""".format(self.title)


@python_2_unicode_compatible
class Album(models.Model):
    """Album class."""

    profile = models.ForeignKey(ImagerProfile,
                                on_delete=models.CASCADE,
                                related_name="albums")

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)

    published = models.CharField(max_length=255,
                                 choices=PUB_STATUS,
                                 default='PU')

    cover_photo = models.ForeignKey(Photo,
                                    related_name='cover',
                                    blank=True,
                                    null=True)

    photos = models.ManyToManyField(
        Photo,
        related_name='in_album',
        blank=True
    )
    tags = TaggableManager()

    def __str__(self):
        """Show string."""
        return """
Album: {}
""".format(self.title)
