from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class ImagerProfile(models.Model):
    """A profile for users to our application"""

    user = models.OneToOneField(User)
    location = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(null=True, blank=True)
    LEVELS = (
        ('beginner', 'Beginner'),
        ('hobbyist', 'Hobbyist'),
        ('professional', 'Professional')
    )
    photog_level = models.CharField(  # required max length?
        choices=LEVELS,
        default='Hobbyist',
        max_length=144
    )
    website = models.URLField()
    headline = models.CharField(
        max_length=144
    )
    is_active = models.BooleanField(default=True)

    def active(self):
        """
        Provides full query functionality limited to profiles for users
        who are active (allowed to log in)
        """
        return self.objects.all().exclude(is_active=False)

    def __repr__(self):
        return self.user.username


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()
