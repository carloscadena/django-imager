from django.test import TestCase, Client
from imager_images.models import Photo
from imager_images.models import Album
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import os
from imagersite.settings import MEDIA_ROOT
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


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


class ProfileTests(TestCase):

    def setUp(self):
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
        to_delete = os.path.join(MEDIA_ROOT, 'photos', 'testing*.png')
        os.system('rm -rf ' + to_delete)

    def test_some_route_lists_images(self):
        response = self.client.get(reverse('profile'))
        self.assertTrue(b'This is the profile page' in response.content)

    def test_upload_image_add_new_photo_instance(self):
        self.assertEqual(Photo.objects.count(), 20)

    def test_new_photo_is_private_by_default(self):
        self.assertEqual(self.photos[0].published, "PV")

    def test_delete_user_with_photos_photos_die(self):
        self.user.delete()
        self.assertTrue(Photo.objects.count() == 0)

    def test_uploaded_photo_lives_in_media_user_photos(self):
        upload_dir = os.path.join(MEDIA_ROOT, 'photos')
        directory_contents = os.listdir(upload_dir)
        name = self.photos[1].image.name.split('/')[1]
        self.assertTrue(name in directory_contents)

    def test_delete_user_with_albums_albums_die(self):
        self.assertTrue(Album.objects.count() == 1)
        self.user.delete()
        self.assertTrue(Album.objects.count() == 0)
