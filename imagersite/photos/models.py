from django.db import models
from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos', null=True)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)

    published = models.CharField(
        max_length=2,
        choices=PUB_STATUS,
        default='PU'
    )

    def __repr__(self):
        return "<Photo: {}>".format(self.title)


@python_2_unicode_compatible
class Album(models.Model):
    """Album class"""

    user = models.ForeignKey(
        ImagerProfile,
        related_name="albums",
        blank=True,
        null=True
    )

    contents = models.ManyToManyField(Photo,
                                      related_name='in_album',
                                      blank=True)

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
