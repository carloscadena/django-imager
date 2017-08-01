"""Test modile for API."""
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import factory
from imager_images.models import Album
from imager_images.models import Photo
from imagersite.settings import MEDIA_ROOT
import os
from rest_framework.test import APITestCase


class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""

    class Meta(object):
        """Meta."""

        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class PhotoFactory(factory.django.DjangoModelFactory):
    """Create photos for testing."""

    class Meta(object):
        """Meta."""

        model = Photo
    title = factory.Sequence(lambda n: "photo{}".format(n))
    image = SimpleUploadedFile(
        name="testing.png",
        content=open(MEDIA_ROOT + '/test/testing.png', 'rb').read(),
        content_type="image/png"
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Create albums for testing."""

    class Meta(object):
        """Meta."""

        model = Album
    title = factory.Sequence(lambda n: "album{}".format(n))


class ApiTests(APITestCase):
    """Tests for the Api."""

    def setUp(self):
        """Set up for testing."""
        user = UserFactory.create()
        user.set_password('caaarlos')
        user.save()
        self.user = user
        photos = [PhotoFactory.create(profile=user.profile) for i in range(20)]
        album = AlbumFactory.build()
        album.profile = user.profile
        album.save()
        for photo in photos:
            album.photos.add(photo)
        album.cover_photo = photos[0]
        album.save()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'photos', 'testing*.png')
        os.system('rm -rf ' + to_delete)

    def test_get_route_status_200(self):
        """Status 200."""
        response = self.client.get(reverse('api'))
        self.assertEqual(response.status_code, 200)

    def test_get_route_sends_photos(self):
        """Sends Json Photos."""
        response = self.client.get(reverse('api'))
        self.assertEqual(
            len(response.json()),
            Photo.objects.count()
        )

    def test_get_route_photos_have_meta_info(self):
        """Meta info on photos from api."""
        response = self.client.get(reverse('api'))
        image_meta = response.json()[0]
        self.assertTrue('title' in image_meta)
        self.assertTrue('description' in image_meta)
        self.assertTrue('profile' in image_meta)
        self.assertTrue('image' in image_meta)
        self.assertTrue('date_uploaded' in image_meta)
        self.assertTrue('date_modified' in image_meta)
        self.assertTrue('date_published' in image_meta)
        self.assertTrue('published' in image_meta)
