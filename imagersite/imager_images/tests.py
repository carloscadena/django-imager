"""Testing suite for Django-Imager"""
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
# from django.urls import reverse_lazy
import factory
from imager_images.models import Photo
from imager_images.models import Album
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from imagersite.settings import MEDIA_ROOT
from bs4 import BeautifulSoup as soup


class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class PhotoFactory(factory.django.DjangoModelFactory):
    """Create photos for testing."""
    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "photo{}".format(n))
    image = SimpleUploadedFile(
        name="testing.png",
        content=open(MEDIA_ROOT + '/test/testing.png', 'rb').read(),
        content_type="image/png"
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Create albums for testing."""
    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "album{}".format(n))


class PhotoAndAlbumTests(TestCase):
    """Photo and Album tests."""

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
        self.photos = photos
        self.album = album
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'photos', 'testing*.png')
        os.system('rm -rf ' + to_delete)

    def test_album_view_status_200(self):
        """Test that the album view returns a status code of 200."""
        response = self.client.get(reverse('albums'))
        self.assertEqual(response.status_code, 200)

    def test_album_view_shows_one_album(self):
        """Test that the Album view shows the one album that was created."""
        response = self.client.get(reverse('albums'))
        html = soup(response.content, "html.parser")
        albums = html.findAll("div", {"class": "album"})
        self.assertTrue(len(albums) == 1)

    def test_photo_view_returns_status_200(self):
        """Test that the photo view returns a status code of 200."""
        response = self.client.get(reverse('photos'))
        self.assertEqual(response.status_code, 200)

    def test_photo_view_has_20_images(self):
        """Test that the photo view shows the 20 images created."""
        response = self.client.get(reverse('photos'))
        html = soup(response.content, "html.parser")
        photos = html.findAll("div", {"class": "photo"})
        self.assertTrue(len(photos) == 20)

    # def test_album_view_with_album_id_returns_status_code_200(self):
    #     """Test that a specific album view returns a status code of 200."""
    #     response = self.client.get(
    #         reverse_lazy('album', kwargs={'album_id': '1'})
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_album_view_with_ID_has_20_images(self):
    #     """Test that an album has 20 images in it."""
    #     pass

    def test_library_view_returns_status_200(self):
        """Test that the library view returns a status code of 200."""
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 200)

    def test_library_view_has_link_to_albums(self):
        """Test that link to the albums is available on the library view."""
        response = self.client.get(reverse('library'))
        html = soup(response.content, "html.parser")
        # import pdb; pdb.set_trace()
        link = html.findAll("a", {"href": "/images/albums/"})
        self.assertTrue(link)

    def test_album_view_incorrect_id_404s(self):
        """Test that an incorrect album ID redirects to the albums page."""
        response = self.client.get(
            reverse('album', kwargs={'album_id': '23'}))
        self.assertTrue(response.status_code == 404)
