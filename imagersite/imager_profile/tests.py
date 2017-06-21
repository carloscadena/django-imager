from django.test import TestCase
from django.contrib.auth.models import User
import factory
from imager_profile.models import ImagerProfile

# Create your tests here.


class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class ProfileTestCase(TestCase):
    """."""
    def setUp(self):
        users = [UserFactory.create() for _ in range(20)]
        self.users = users

    def test_every_profile_must_have_a_user(self):
        """Test that every profile has a user."""
        with self.assertRaises(Exception):
            imager = ImagerProfile()
            imager.save()

    def test_profile_with_user_prints_username(self):
        """Test that profile with user prints username."""
        a_profile = ImagerProfile.objects.first()
        self.assertTrue(str(a_profile), a_profile.user.username)

    def test_new_user_has_a_profile(self):
        """Test new user has a profile."""
        user = UserFactory.create()
        profile = ImagerProfile.objects.last()
        self.assertTrue(profile.user == user)

    def test_profile_with_user_photog_level_beginner(self):
        """Test that photography level could be begginer."""
        profile = ImagerProfile.objects.last()
        profile.photog_level = "Beginner"
        profile.save()
        self.assertEqual(profile.photog_level, 'Beginner')

    def test_profile_with_user_photog_level_hobbyist(self):
        """Test that photography level could be hobbyist."""
        profile = ImagerProfile.objects.last()
        profile.photog_level = "Hobbyist"
        profile.save()
        self.assertEqual(profile.photog_level, 'Hobbyist')

    def test_profile_with_user_photog_level_professional(self):
        """Test that photography level could be professional."""
        profile = ImagerProfile.objects.last()
        profile.photog_level = "Professional"
        profile.save()
        self.assertEqual(profile.photog_level, 'Professional')

    def test_profiles_equals_users(self):
        """Every created user has a profile."""
        self.assertTrue(ImagerProfile.objects.count() == 20)

    def test_is_active_method(self):
        """Test newly created users are active."""
        self.assertTrue(ImagerProfile.objects.first().is_active is True)
