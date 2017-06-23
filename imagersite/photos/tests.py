# from django.test import TestCase, Client
# from Photo.models import Photo
# from Photo.models import Album
# import factory
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse
# import os
#
#
# class PhotoFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Photo
#     title = factory.Sequence(lambda n: "photo{}".format(n))
#     user = factory.Sequence(lambda n: "person{}".format(n))
#     cover = SimpleUploadedFile(
#         name="foofile.jpg",
#         content=open('/Users/nick/Downloads/malcolmx.jpg', 'rb').read(),
#         content_type="image/jpeg"
#     )
#
#
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#
#
# class PhotoTests(TestCase):
#
#     def setUp(self):
#         photos = [PhotoFactory.create() for i in range(20)]
#         self.photos = photos
#         self.client = Client()
#
#     def tearDown(self):
#         to_delete = os.path.join(BASE_DIR, 'photo_covers', '*.jpg')
#         os.system('rm -rf ' + to_delete)
#
#     def test_some_route_lists_images(self):
#         response = self.client.get(reverse('profile'))
