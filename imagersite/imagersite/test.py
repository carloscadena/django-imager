# """."""
# from bs4 import BeautifulSoup
# from django.contrib.auth.models import User
# from django.core import mail
# from django.test import Client
# from django.test import RequestFactory
# from django.test import TestCase
# from django.urls import reverse
# from imagersite.views import home_view
#
#
# class ViewTest(TestCase):
#     """."""
#
#     def setUp(self):
#         """."""
#         self.client = Client()
#         self.ger_request = RequestFactory().get('/foo')
# 
#     def test_home_route_returns_status_200(self):
#         """."""
#         response = self.client.get(reverse('home'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_home_view_somthing(self):
#         """."""
#         response = home_view(self.ger_request)
#         self.assertTrue(b'h1' in response.content)
#
#
# class RegistrationTests(TestCase):
#     """."""
#
#     def setUp(self):
#         """."""
#         self.client = Client()
#
#     def test_registration_page_uses_proper_template(self):
#         """Registration is returned."""
#         response = self.client.get(reverse('registration_register'))
#         self.assertIn(
#             'registration/registration_form.html',
#             response.template_name
#         )
#
#     def test_resgistartion_creates_new_inactive_user(self):
#         """."""
#         self.assertTrue(User.objects.count() == 0)
#         response = self.client.get(reverse('registration_register'))
#         html = BeautifulSoup(response.rendered_content, "html.parser")
#         # import pdb; pdb.set_trace()
#         token = html.find(
#             'input', {'name': "csrfmiddlewaretoken"}
#         ).attrs['value']
#         info = {
#             'csrfmiddlewaretoken': token,
#             'username': 'test',
#             'email': 'test@test.com',
#             'password1': 'testtest123',
#             'password2': 'testtest123'
#         }
#         self.client.post(
#             reverse('registration_register'),
#             info
#         )
#         self.assertFalse(User.objects.first().is_active)
#         self.assertTrue(len(mail.outbox) == 1)
