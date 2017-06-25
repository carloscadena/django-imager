from django.test import TestCase, Client
from imager_images.models import Photo
from imager_images.models import Album
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os
from imagersite.settings import MEDIA_ROOT
# from imager_profile.models import ImagerProfile
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


# class ProfileFactory(factory.django.DjangoModelFactory):
#     """Setting up users for tests."""
#     class Meta:
#         model = ImagerProfile


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "photo{}".format(n))
    image = SimpleUploadedFile(
        name="testing.png",
        content=open(MEDIA_ROOT + '/test/testing.png', 'rb').read(),
        content_type="image/png"
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "album{}".format(n))
    # profile = ProfileFactory.create()
    cover = SimpleUploadedFile(
        name="testing.png",
        content=open(MEDIA_ROOT + '/test/testing.png', 'rb').read(),
        content_type="image/png"
    )


class ProfileTests(TestCase):

    def setUp(self):
        user = UserFactory()
        # profile = ProfileFactory.create()
        photos = [PhotoFactory.create(profile=user.profile) for i in range(20)]
        album = AlbumFactory.create(profile=user.profile, photos=photos)
        self.photos = photos
        self.album = album
        self.client = Client()

    def tearDown(self):
        to_delete = os.path.join(MEDIA_ROOT, 'test', '*.png')
        os.system('rm -rf ' + to_delete)

    def test_some_route_lists_images(self):
        response = self.client.get(reverse('profile'))
        self.assertTrue(b'This is the profile page' in response.content)
