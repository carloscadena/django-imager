"""Django Models Modules."""
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encodeing import python_2_unicode_compatible


class ImagerActiveProfile(models.Manager):
    """."""

    def get_queryset(self):
        """."""
        super(ImagerActiveProfile, self).get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """A profile for users to our application."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True)
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
        max_length=25
    )
    website = models.URLField()
    headline = models.CharField(
        max_length=144,
        null=True,
        Blank=True
    )
    objects = models.Manager()
    active = ImagerActiveProfile()

    @property
    def is_active(self):
        """."""
        return self.user.is_active

        # is_active = models.BooleanField(default=True)

    # def active(self):
    #     """Provide full query functionality.
    #
    #     limited to profiles for users who are active (allowed to log in)
    #     """
    #     return self.objects.all().exclude(is_active=False)
    #
    def __repr__(self):
        """Print displays username."""
        return """
User name: {}
""".format(self.user.username)


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    """All users get profile added."""
    if kwargs['created']:
        new_profile = ImagerProfile(
            user=kwargs['instance']
        )
        new_profile.save()
