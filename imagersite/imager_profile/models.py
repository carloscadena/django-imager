"""Django Models Modules."""
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


class ImagerActiveProfile(models.Manager):
    """Profile has been activated"""

    def get_queryset(self):
        """Allow an active user to use site as actived user."""
        return super(ImagerActiveProfile, self).get_queryset().filter(
            user__is_active=True
        )


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    """A profile for users to our application."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    location = models.CharField(max_length=50, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(null=True, blank=True)
    LEVELS = (
        ('beginner', 'Beginner'),
        ('hobbyist', 'Hobbyist'),
        ('professional', 'Professional')
    )
    photog_level = models.CharField(
        choices=LEVELS,
        default='Hobbyist',
        max_length=25
    )
    website = models.URLField()
    headline = models.CharField(
        max_length=144,
        null=True,
        blank=True
    )
    objects = models.Manager()
    active = ImagerActiveProfile()

    @property
    def is_active(self):
        """True of false if User has been activated."""
        return self.user.is_active

    def __str__(self):
        """Print displays username."""
        return """
User name: {}
""".format(self.user.username)

    def __repr__(self):
        """Show username."""
        return """
User name: {}
""".format(self.user.username)


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, instance, **kwargs):
    """All users get profile added."""
    if kwargs['created']:
        new_profile = ImagerProfile(user=instance)
        new_profile.save()
