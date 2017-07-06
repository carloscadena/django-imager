"""Test for registration view."""
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from imagersite.views import home_view


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
