"""Testing suite for Django-Imager."""
from bs4 import BeautifulSoup as soup
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
import factory
from imager_images.models import Album
from imager_images.models import Photo
from imagersite.settings import MEDIA_ROOT
import os


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
        photos[0].tags.add('testtag')
        photos[0].save()
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
        response = self.client.get(reverse('albums', kwargs={'page_num': 1}))
        self.assertEqual(response.status_code, 200)

    def test_album_view_shows_one_album(self):
        """Test that the Album view shows the one album that was created."""
        response = self.client.get(reverse('albums', kwargs={'page_num': 1}))
        html = soup(response.content, "html.parser")
        albums = html.findAll("div", {"class": "album"})
        self.assertTrue(len(albums) == 1)

    def test_photo_view_returns_status_200(self):
        """Test that the photo view returns a status code of 200."""
        response = self.client.get(reverse('photos', kwargs={'page_num': 1}))
        self.assertEqual(response.status_code, 200)

    def test_photo_view_has_3_images(self):
        """Test that the photo view shows the 20 images created."""
        response = self.client.get(reverse('photos', kwargs={'page_num': 1}))
        html = soup(response.content, "html.parser")
        photos = html.findAll("div", {"class": "photo"})
        self.assertTrue(len(photos) == 3)

    def test_album_view_with_album_id_returns_status_code_200(self):
        """Test that a specific album view returns a status code of 200."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse_lazy('album', kwargs={'album_id': album_id, 'page_num': 1})
        )
        self.assertEqual(response.status_code, 200)

    def test_album_with_ID_has_20_images_in_it(self):
        """Test that an album has 20 images in it."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse_lazy('album', kwargs={'album_id': album_id, 'page_num': 1})
        )
        self.assertEqual(response.context_data['photos'].paginator.count, 20)

    def test_library_view_returns_status_200(self):
        """Test that the library view returns a status code of 200."""
        response = self.client.get(reverse(
            'library',
            kwargs={'album_page_num': 1, 'photo_page_num': 1}
        ))
        self.assertEqual(response.status_code, 200)

    def test_library_view_has_link_to_albums(self):
        """Test that link to the albums is available on the library view."""
        response = self.client.get(reverse(
            'library',
            kwargs={'album_page_num': 1, 'photo_page_num': 1})
        )
        html = soup(response.content, "html.parser")
        link = html.findAll("a", {"href": "/images/albums/page/1"})
        self.assertTrue(link)

    def test_library_view_displays_public_albums(self):
        """Test that the library view shows all public albums"""
        response = self.client.get(reverse(
            'library',
            kwargs={'album_page_num': 1, 'photo_page_num': 1})
        )
        html = soup(response.rendered_content, "html.parser")
        albums = html.findAll('div', {'class': 'album'})
        self.assertTrue(len(albums) == 1)

    def test_library_view_displays_public_photos(self):
        """Test that the library view shows all public photos"""
        response = self.client.get(reverse(
            'library',
            kwargs={'album_page_num': 1, 'photo_page_num': 1})
        )
        html = soup(response.rendered_content, "html.parser")
        photos = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(photos) == 3)

    def test_album_view_incorrect_id_404s(self):
        """Test that an incorrect album ID redirects to the albums page."""
        response = self.client.get(
            reverse('album', kwargs={'album_id': '23', 'page_num': 1}))
        self.assertTrue(response.status_code == 404)

    def test_album_names_display_on_library_page(self):
        """Test that the album name displays with albums on library page."""
        response = self.client.get(reverse(
            'library',
            kwargs={'album_page_num': 1, 'photo_page_num': 1})
        )
        self.assertTrue(b'<p>album' in response.content)

# Taggit Tests ============================================

    def test_tags_show_on_photos_view(self):
        """Test tags show on photos view."""
        response = self.client.get(
            reverse('photos', kwargs={'page_num': 1})
        )
        self.assertTrue(b'testtag' in response.content)

    def test_tags_show_on_library_view(self):
        """Test Tags show on library view."""
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}
            )
        )
        self.assertTrue(b'testtag' in response.content)

    def test_tags_show_on_individual_album_page(self):
        """Test tags show on individual album page."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse(
                'album',
                kwargs={'album_id': album_id, 'page_num': 1}
            )
        )
        self.assertTrue(b'testtag' in response.content)

    def test_tags_link_to_more_photos_with_same_tag(self):
        """Test tags link to more photos with the same tag."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse(
                'album',
                kwargs={'album_id': album_id, 'page_num': 1}
            )
        )
        html = soup(response.rendered_content, "html.parser")
        link = html.findAll('a', {'href': '/images/tagged/testtag'})
        self.assertTrue(link)
        response = self.client.get(reverse(
            'tagged_photos',
            kwargs={'slug': 'testtag'})
        )
        html = soup(response.rendered_content, "html.parser")
        link = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(link) == 1)

    def test_tags_can_be_added_to_photos(self):
        """Test tags can be added to photos."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        photo_id = Photo.objects.all()[0].id
        response = self.client.get(reverse(
            'photo_edit',
            kwargs={'photo_id': photo_id})
        )
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        info = {
            'title': 'photo name',
            'description': 'a description',
            'tags': 'basketball',
            'published': 'PU',
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('photo_edit', kwargs={'photo_id': photo_id}),
            info,
            follow=True
        )
        html = soup(response.content, "html.parser")
        self.assertTrue(b'basketball' in response.content)

    def test_tags_can_be_edited_on_photos(self):
        """Test tags can be edited on photos."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        photo_id = Photo.objects.all()[0].id
        response = self.client.get(reverse(
            'photo_edit',
            kwargs={'photo_id': photo_id})
        )
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        info = {
            'title': 'photo name',
            'description': 'a description',
            'tags': 'seals',
            'published': 'PU',
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('photo_edit', kwargs={'photo_id': photo_id}),
            info,
            follow=True
        )
        html = soup(response.content, "html.parser")
        self.assertTrue(b'seals' in response.content)

# Pagination tests ==================================

    def test_library_page_has_only_3_photos(self):
        """Test that the library page does not show more than 3 photos."""
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}),
        )
        html = soup(response.rendered_content, "html.parser")
        photos = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(photos) == 3)

    def test_library_page_shows_only_3_albums(self):
        """Test that the library page only shows 3 albums."""
        for _ in range(3):
            album = AlbumFactory.build()
            album.profile = self.user.profile
            album.save()
            for photo in self.photos:
                album.photos.add(photo)
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}),
        )
        html = soup(response.rendered_content, "html.parser")
        albums = html.findAll('div', {'class': 'album'})
        self.assertTrue(len(albums) == 3)

    def test_library_page_pagination_next_set_of_three_photos(self):
        """Test that the photos are paginated by 3."""
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}),
        )
        self.assertTrue(b'library/1/2' in response.content)
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 2}),
        )
        html = soup(response.rendered_content, "html.parser")
        photos = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(photos) == 3)

    def test_library_page_pagination_previous_set_of_three_photos(self):
        """Test that the photos are paginated by 3."""
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 2}),
        )
        self.assertTrue(b'library/1/1' in response.content)

    def test_photo_page_has_only_3_photos(self):
        """Test that the library page does not show more than 3 photos."""
        response = self.client.get(
            reverse(
                'photos',
                kwargs={'page_num': 1}),
        )
        html = soup(response.rendered_content, "html.parser")
        photos = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(photos) == 3)

    def test_photo_page_pagination_next_set_of_three_photos(self):
        """Test that the photos are paginated by 3."""
        response = self.client.get(
            reverse(
                'photos',
                kwargs={'page_num': 1}),
        )
        self.assertTrue(b'photos/page/2' in response.content)
        response = self.client.get(
            reverse(
                'photos',
                kwargs={'page_num': 2}),
        )
        html = soup(response.rendered_content, "html.parser")
        photos = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(photos) == 3)

    def test_photo_page_pagination_previous_set_of_three_photos(self):
        """Test that the photos are paginated by 3."""
        response = self.client.get(
            reverse(
                'photos',
                kwargs={'page_num': 2}),
        )
        self.assertTrue(b'photos/page/1' in response.content)

    def test_album_page_has_only_3_albums(self):
        """Test that the library page does not show more than 3 albums."""
        for _ in range(3):
            album = AlbumFactory.build()
            album.profile = self.user.profile
            album.save()
            for photo in self.photos:
                album.photos.add(photo)
        response = self.client.get(
            reverse(
                'albums',
                kwargs={'page_num': 1}),
        )
        html = soup(response.rendered_content, "html.parser")
        albums = html.findAll('div', {'class': 'album'})
        self.assertTrue(len(albums) == 3)

    def test_album_page_pagination_next_set_of_three_albums(self):
        """Test that the albums are paginated by 3."""
        for _ in range(3):
            album = AlbumFactory.build()
            album.profile = self.user.profile
            album.save()
            for photo in self.photos:
                album.photos.add(photo)
        response = self.client.get(
            reverse(
                'albums',
                kwargs={'page_num': 2}),
        )
        html = soup(response.rendered_content, "html.parser")
        albums = html.findAll('div', {'class': 'album'})
        self.assertTrue(len(albums) == 1)

    def test_album_page_pagination_previous_set_of_three_albums(self):
        """Test that the albums are paginated by 3."""
        for _ in range(3):
            album = AlbumFactory.build()
            album.profile = self.user.profile
            album.save()
            for photo in self.photos:
                album.photos.add(photo)
        response = self.client.get(
            reverse(
                'albums',
                kwargs={'page_num': 2}),
        )
        self.assertTrue(b'albums/page/1' in response.content)

    def test_single_album_page_has_only_3_photos(self):
        """Test that an album page does not show more than 3 photos."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse(
                'album',
                kwargs={'album_id': album_id, 'page_num': 1}),
        )
        html = soup(response.rendered_content, "html.parser")
        photos = html.findAll('div', {'class': 'photo'})
        self.assertTrue(len(photos) == 3)

    def test_single_album_page_pagination_next_set_of_three_photos(self):
        """Test that the photos in an album are paginated by 3."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse(
                'album',
                kwargs={'album_id': album_id, 'page_num': 1}),
        )
        # import pdb; pdb.set_trace()
        self.assertTrue(b'album/' + str(album_id).encode(encoding='UTF-8') + b'/2' in response.content)

    def test_single_album_page_pagination_previous_set_of_three_photos(self):
        """Test that the photos in a single album are paginated by 3."""
        album_id = Album.objects.all()[0].id
        response = self.client.get(
            reverse(
                'album',
                kwargs={'album_id': album_id, 'page_num': 2}),
        )
        self.assertTrue(b'album/' + str(album_id).encode(encoding='UTF-8') + b'/1' in response.content)

# Test Photo and Album creation functionality

    def test_album_create_view_status_code_200(self):
        """Test the album create view returns status code 200."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('album_add'))
        self.assertTrue(response.status_code == 200)

    def test_album_create_view_not_logged_in_status_code_302(self):
        """Test the album create view returns status code 302."""
        response = self.client.get(reverse('album_add'))
        self.assertTrue(response.status_code == 302)

    def test_photo_create_view_returns_status_code_200(self):
        """Test that the photo create view returns status code 200.."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('photo_add'))
        self.assertTrue(response.status_code == 200)

    def test_photo_create_view_not_logged_inreturns_status_code_302(self):
        """Test that the photo create view returns status code 302."""
        response = self.client.get(reverse('photo_add'))
        self.assertTrue(response.status_code == 302)

    def test_library_view_has_buttons_to_photo_create(self):
        """Test library view has buttons to add photo."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}
            )
        )
        self.assertTrue(
            reverse('photo_add').encode('utf-8') in response.content
        )

    def test_library_view_has_button_to_album_create(self):
        """Test library view has buttons to add album."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(
            reverse(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}
            )
        )
        self.assertTrue(
            reverse('album_add').encode('utf-8') in response.content
        )

    def test_create_album_view_has_correct_fields(self):
        """Test create album view has correct fields for adding new."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('album_add'))
        html = soup(response.content, "html.parser")
        field = html.findAll('input', {'name': 'title'})
        self.assertTrue(field)

    def test_create_photo_view_has_correct_fields(self):
        """Test create photo view has correct fields for adding new."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('photo_add'))
        html = soup(response.content, "html.parser")
        field = html.findAll('input', {'name': 'title'})
        self.assertTrue(field)

    def test_ability_to_assign_photos_in_album_create_view(self):
        """Test that album create view has ability to assign photos."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('album_add'))
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        info = {
            'title': 'album name',
            'description': 'a description',
            'published': 'PU',
            'photos': [1, 2, 3],
            'cover_photo': 1,
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('album_add'),
            info,
            follow=True
        )
        self.assertTrue(user.profile.albums.count() == 2)

    def test_after_create_photo_redirects_to_library(self):
        """Test that after you create photo you are redirected to library."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('photo_add'))
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        image = SimpleUploadedFile(
            name="testing.png",
            content=open(MEDIA_ROOT + '/test/testing.png', 'rb').read(),
            content_type="image/png"
        )
        info = {
            'image': image,
            'title': 'photo name',
            'description': 'a description',
            'published': 'PU',
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('photo_add'),
            info
        )
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.url == '/images/library/1/1')

    def test_after_album_create_redirects_to_library(self):
        """Test that after you create album you are redirected to library."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('album_add'))
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        info = {
            'title': 'album name',
            'description': 'a description',
            'published': 'PU',
            'photos': [21, 22, 23],
            'cover_photo': 21,
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('album_add'),
            info
        )
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.url == '/images/library/1/1')

    def test_required_fields_on_photo_create_must_be_filled(self):
        """Test required fields are actually required in photo create."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('photo_add'))
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        info = {
            'title': 'photo name',
            'description': 'a description',
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('photo_add'),
            info
        )
        self.assertTrue(b'This field is required.' in response.content)

    def test_required_fields_on_album_create_must_be_filled(self):
        """Test required fields are actually required in album create."""
        user = User.objects.all()[0]
        self.client.force_login(user)
        response = self.client.get(reverse('album_add'))
        html = soup(response.rendered_content, "html.parser")
        token = html.findAll('input', {'name': "csrfmiddlewaretoken"})
        info = {
            'title': 'album name',
            'description': 'a description',
            'csrfmiddlewaretoken': token[0]['value']
        }
        response = self.client.post(
            reverse('album_add'),
            info
        )
        self.assertTrue(b'This field is required.' in response.content)
