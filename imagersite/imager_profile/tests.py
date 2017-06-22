"""Testing suite for Django-Imager"""
# from bs4 import BeautifulSoup as soup
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import factory
from imager_profile.models import ImagerProfile
from imagersite.views import home_view


class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class ProfileTestCase(TestCase):
    """Test suite for creating new users."""
    def setUp(self):
        """Set up users for testing."""
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


class ProfileViewTests(TestCase):
    """A class to run tests on the profile view."""

    def setUp(self):
        """Set up for profile view tests."""
        self.client = Client()
        self.req_factory = RequestFactory()

    # # must make link on web page for test to work
    # def test_link_button_on_home_page_appears(self):
    #     """."""
    #     response = self.client(reverse('home'))
    #     self.assertTrue(b'a href="/"' in response.content)

    def test_home_view_responds_200(self):
        """Test that the home view returns a status code of 200."""
        get_req = self.req_factory.get('/foo')
        response = home_view(get_req)
        self.assertTrue(response.status_code == 200)

    def test_if_user_isnt_authenticated_shows_login(self):
        """Test that login is available when user isn't authenticated."""
        response = self.client.get(reverse('home'))
        self.assertTrue(b'login' in response.content.lower())

    def test_if_user_is_authenticated_shows_logout(self):
        """Test that logout is available when user is logged in."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        response = self.client.get(reverse('home'))
        self.assertFalse(b'login' in response.content.lower())
        self.assertTrue(b'logout' in response.content.lower())

    def test_if_user_is_authenticated_and_logout_no_longer_authenticated(self):
        """Test that logout properly logs out the user."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        response = self.client.get(reverse('logout'), follow=True)
        self.assertTrue(b'login' in response.content.lower())

    def test_no_of_users_equals_no_of_profiles(self):
        """
        Test that the same amount of users
        and profiles have been created in db.
        """
