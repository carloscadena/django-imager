from django.test import TestCase
from django.contrib.auth.models import User
import factory
from imager_profile.models import ImagerProfile

# Create your tests here.


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


# class ImagerFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = ImagerProfile
#     location = factory.Faker('state')
#     creation_date = factory.Faker('')
#     birthday = models.DateField(null=True, blank=True)
#     LEVELS = (
#         ('beginner', 'Beginner'),
#         ('hobbyist', 'Hobbyist'),
#         ('professional', 'Professional')
#     )
#     photog_level = models.CharField(  # required max length?
#         choices=LEVELS,
#         default='Hobbyist',
#         max_length=144
#     )
#     website = models.URLField()
#     headline = factory.Faker(
#         max_length=144
#     )
#     is_active = models.BooleanField(default=True)


class ProfileTestCase(TestCase):
    """."""
    def setUp(self):
        # imager = ImagerFactory.create()
        user = UserFactory.create()
        # imager.save()
        user.save()
        self.user = user

    def test_every_profile_must_have_a_user(self):
        with self.assertRaises(Exception):
            imager = ImagerProfile()
            imager.save()

    def test_profile_with_user_prints_username(self):
        a_profile = ImagerProfile.objects.first()
        self.assertTrue(str(a_profile), a_profile.user.username)

    def test_new_user_has_a_profile(self):
        """."""
        user = UserFactory.create()
        profile = ImagerProfile.objects.last()
        self.assertTrue(profile.user == user)


    def test_profile_with_user_photog_level_beginner(self):
        imager = ImagerProfile()
        imager.user = self.user
        imager.photog_level = 'Beginner'
        imager.save()
        self.assertEqual(imager.photog_level, 'Beginner')


    def test_profile_with_user_photog_level_hobbyist(self):
        imager = ImagerProfile()
        imager.user = self.user
        imager.photog_level = 'Hobbyist'
        imager.save()
        self.assertEqual(imager.photog_level, 'Hobbyist')

    def test_profile_with_user_photog_level_professional(self):
        imager = ImagerProfile()
        imager.user = self.user
        imager.photog_level = 'Professional'
        imager.save()
        self.assertEqual(imager.photog_level, 'Professional')

    # Should fail? Need clarification
    def test_profile_with_user_photog_level_bad_data(self):
        imager = ImagerProfile()
        imager.user = self.user
        imager.photog_level = 'something'
        imager.save()
        self.assertEqual(imager.photog_level, 'something')
