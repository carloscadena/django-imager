from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from imager_profile.models import ImagerProfile


PUB_STATUS = (
    ('PR', 'Private'),
    ('SH', 'Shared'),
    ('PU', 'Public')
)


@python_2_unicode_compatible
class Photo(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)
    profile = models.ForeignKey(ImagerProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)

    published = models.CharField(
        max_length=2,
        choices=PUB_STATUS,
        default='PV'
    )

    def __repr__(self):
        return "<Photo: {}>".format(self.title)

    def __str__(self):
        """Show string."""
        return """
Photo: {}
""".format(self.title)


@python_2_unicode_compatible
class Album(models.Model):
    """Album class"""

    profile = models.ForeignKey(ImagerProfile, on_delete=models.CASCADE)

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

    def __str__(self):
        """Show string."""
        return """
Album: {}
""".format(self.title)
