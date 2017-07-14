"""Test for registration view."""

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from imagersite.views import home_view
from django.urls import reverse_lazy
from imager_images.models import Photo
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class ViewTest(TestCase):
    """Test Home View"""

    def setUp(self):
        """Setup home fixture"""
        self.client = Client()
        self.ger_request = RequestFactory().get('/')

    def test_home_route_returns_status_200(self):
        """Home route returns 200."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_has_some_heading(self):
        """Has heading"""
        response = home_view(self.ger_request)
        self.assertTrue(b'h1' in response.content)


class RegistrationTests(TestCase):
    """Test Registration."""

    def setUp(self):
        """Make Reg"""
        self.client = Client()

    def test_registration_page_uses_proper_template(self):
        """Registration is returned."""
        response = self.client.get(reverse('registration_register'))
        self.assertIn(
            'registration/registration_form.html',
            response.template_name
        )

    def test_registration_creates_new_inactive_user(self):
        """Register adds user."""
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, "html.parser")
        token = html.find(
            'input', {'name': "csrfmiddlewaretoken"}
        ).attrs['value']
        info = {
            'csrfmiddlewaretoken': token,
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'testtest123',
            'password2': 'testtest123'
        }
        self.client.post(
            reverse('registration_register'),
            info
        )
        self.assertFalse(User.objects.first().is_active)
        self.assertTrue(len(mail.outbox) == 1)

    def test_registration_success_redirects_to_reg_complete_html(self):
        """Test that the registration complete page shows after registering."""
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, "html.parser")
        token = html.find(
            'input', {'name': "csrfmiddlewaretoken"}
        ).attrs['value']
        info = {
            'csrfmiddlewaretoken': token,
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'testtest123',
            'password2': 'testtest123'
        }
        response = self.client.post(
            reverse('registration_register'),
            info,
            follow=True
        )
        self.assertIn(
            'Registration complete',
            response.rendered_content
        )

    def test_activation_key_activates_user(self):
        self.assertTrue(User.objects.count() == 0)
        response = self.client.get(reverse('registration_register'))
        html = BeautifulSoup(response.rendered_content, "html.parser")
        token = html.find(
            'input', {'name': "csrfmiddlewaretoken"}
        ).attrs['value']
        info = {
            'csrfmiddlewaretoken': token,
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'testtest123',
            'password2': 'testtest123'
        }
        response = self.client.post(
            reverse('registration_register'),
            info
        )
        key = response.context['activation_key']
        response = self.client.get(
            "/accounts/activate/" + key + "/",
            follow=True
        )
        self.assertIn('Activated!!', response.rendered_content)


#  ========================= Tests from class July 13 ========================


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Sequence(lambda n: "photo{}".format(n))
    image = SimpleUploadedFile(
        name='somephoto.jpg',
        content=open(os.path.join(BASE_DIR, 'MEDIA', 'test', 'testing.png'), 'rb').read(),
        content_type='image/jpeg'
    )


class HomePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='carl', email='carl@carl.carl')
        self.user.save()

    def add_photos(self):
        photos = [PhotoFactory.build() for _ in range(1)]
        for photo in photos:
            photo.profile = self.user.profile
            photo.save()

    def test_when_no_images_placeholder_appears(self):
        response = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(html.find('img', {'src': '/static/imagersite/testing.png'}))

    def test_when_images_exist_one_of_them_is_on_the_page(self):
        self.add_photos()
        response = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(response.content, 'html.parser')
        img_tag = html.find_all('img')
        self.assertTrue(img_tag[0].attrs['src'] == Photo.objects.first().image.url)


class ProfilePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='carl', email='carl@carl.carl')
        self.user.set_password('bobloblaw')
        self.user.save()

    def test_user_profile_info_on_profile_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('profile', kwargs={'username': 'carl'}))
        self.assertTrue(b'<p>Username: carl</p>' in response.content)

    def test_user_profile_page_has_link_to_library_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('profile', kwargs={'username': 'carl'}))
        html = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(html.find('a', {'href': '/images/library/'}))

    def test_when_user_logs_in_redirect_to_profile_page(self):
        response = self.client.post(reverse_lazy('login'), {
            'username': self.user.username, 'password': 'bobloblaw'
        }, follow=True)
        # import pdb; pdb.set_trace()
        self.assertTrue(b'<p>Username: carl</p>' in response.content)
