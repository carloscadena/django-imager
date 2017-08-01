"""Views for displaying images and albums."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from imager_images.models import Album
from imager_images.models import Photo
from imager_profile.models import ImagerProfile
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PhotosView(TemplateView):
    """View for the publicly uploaded albums."""

    template_name = "imager_images/photos.html"
    context_object_name = 'photos'

    def get_context_data(self, slug=None, page_num=1):
        """Get photos."""
        if not slug:
            photos = Photo.objects.filter(published="PU").all()
        else:
            photos = Photo.objects.filter(
                published="PU",
                tags__slug=slug
            ).all()
        photo_pages = Paginator(photos, 3)

        try:
            photo_page = photo_pages.page(page_num)
        except PageNotAnInteger:
            photo_page = photo_pages.page(1)
        except EmptyPage:
            photo_page = photo_pages.page(1)

        context = {
            'photos': photo_page,
            'tags': Tag.objects.all()
        }
        # import pdb; pdb.set_trace()
        return context


class AlbumsView(TemplateView):
    """View for the publicly uploaded albums."""

    template_name = "imager_images/albums.html"
    context_object_name = 'albums'

    def get_context_data(self, page_num=1):
        """Get albums."""

        albums = Album.objects.filter(published="PU").all()
        album_pages = Paginator(albums, 3)

        try:
            album_page = album_pages.page(page_num)
        except PageNotAnInteger:
            album_page = album_pages.page(1)
        except EmptyPage:
            album_page = album_pages.page(1)

        context = {
            'albums': album_page,
        }
        return context


class LibraryView(TemplateView):
    """View for library page."""

    template_name = "imager_images/library.html"

    def get_context_data(self, album_page_num=1, photo_page_num=1):
        """Get albums and photos."""
        album_pages = Paginator(Album.objects.filter(published="PU").all(), 3)
        photo_pages = Paginator(Photo.objects.filter(published="PU").all(), 3)

        try:
            photo_page = photo_pages.page(photo_page_num)
        except PageNotAnInteger:
            photo_page = photo_pages.page(1)
        except EmptyPage:
            photo_page = photo_pages.page(1)

        try:
            album_page = album_pages.page(album_page_num)
        except PageNotAnInteger:
            album_page = album_pages.page(1)
        except EmptyPage:
            album_page = album_pages.page(1)

        context = {
            'albums': album_page,
            'photos': photo_page,
            'tags': Tag.objects.all()
        }
        return context


class AlbumView(TemplateView):
    """View for the publicly uploaded albums."""

    template_name = "imager_images/photos.html"
    context_object_name = 'photos'

    def get_context_data(self, album_id, page_num=1):
        """Get album photos."""
        album = get_object_or_404(Album, id=album_id, published="PU")
        photo_pages = Paginator(album.photos.all(), 3)

        try:
            photo_page = photo_pages.page(page_num)
        except PageNotAnInteger:
            photo_page = photo_pages.page(1)
        except EmptyPage:
            photo_page = photo_pages.page(1)

        context = {
            'photos': photo_page,
            'album': album,
            'tags': Tag.objects.all()
        }
        # import pdb; pdb.set_trace()
        return context


class PhotoAdd(LoginRequiredMixin, CreateView):
    """Class based view for adding a photo."""

    template_name = "imager_images/add_new.html"
    model = Photo
    fields = [
        'image',
        'title',
        'description',
        'published',
        'tags'
    ]

    success_url = reverse_lazy(
        "library",
        kwargs={'album_page_num': 1, 'photo_page_num': 1}
    )
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        """Form should update the profile."""
        self.object = form.save(commit=False)
        self.object.profile = ImagerProfile.objects.get(user=self.request.user)
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class AlbumAdd(LoginRequiredMixin, CreateView):
    """View for adding an album."""

    template_name = "imager_images/add_new.html"
    model = Album
    fields = [
        'photos',
        'title',
        'description',
        'published',
        'cover_photo'
    ]

    success_url = reverse_lazy(
        "library",
        kwargs={'album_page_num': 1, 'photo_page_num': 1}
    )
    login_url = reverse_lazy("login")

    def get_form(self):
        """Retrieve form and make sure can only see own photos."""
        form = super(AlbumAdd, self).get_form()
        form.fields['cover_photo'].queryset = self.request.user.profile.photos.all()
        form.fields['photos'] = forms.ModelMultipleChoiceField(
            queryset=Photo.objects.filter(profile=self.request.user.profile),
            widget=forms.CheckboxSelectMultiple()
        )
        return form

    def form_valid(self, form):
        """Form should update the profile."""
        self.object = form.save(commit=False)
        self.object.profile = ImagerProfile.objects.get(user=self.request.user)
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class PhotoEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for editing a photo."""

    template_name = "imager_images/edit.html"
    pk_url_kwarg = "photo_id"
    model = Photo
    fields = [
        'title',
        'description',
        'published',
        'tags'
    ]
    success_url = reverse_lazy(
        "library",
        kwargs={'album_page_num': 1, 'photo_page_num': 1}
    )
    login_url = reverse_lazy("login")

    def test_func(self):
        """Override userpassestest test_func.

        Checks user making post owns Photo.
        """
        photo = Photo.objects.get(id=self.kwargs['photo_id'])
        return photo.profile.user == self.request.user


class AlbumEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for editing an album."""

    template_name = "imager_images/edit.html"
    pk_url_kwarg = "album_id"
    success_url = reverse_lazy(
        "library",
        kwargs={'album_page_num': 1, 'photo_page_num': 1}
    )
    model = Album
    fields = ['photos',
              'title',
              'description',
              'published',
              'cover_photo']

    def test_func(self):
        """Override the userpassestest test_func.

        Checks user making post owns Album.
        """
        album = Album.objects.get(id=self.kwargs['album_id'])
        return album.profile.user == self.request.user

    def get_form(self):
        """Retrieve form and make sure can only see own photos."""
        form = super(AlbumEdit, self).get_form()
        form.fields['cover_photo'].queryset = self.request.user.profile.photos.all()
        form.fields['photos'] = forms.ModelMultipleChoiceField(
            queryset=Photo.objects.filter(profile=self.request.user.profile),
            widget=forms.CheckboxSelectMultiple()
        )
        return form
