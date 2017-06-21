"""."""
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from imagersite.views import home_view


class ViewTest(TestCase):
    """."""

    def setUp(self):
        """."""
        self.client = Client()
        self.ger_request = RequestFactory().get('/foo')

    def test_home_route_returns_status_200(self):
        """."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_somthing(self):
        """."""
        response = home_view(self.ger_request)
        self.assertTrue(b'h1' in response.content)
