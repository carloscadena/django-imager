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


class LibraryView(TemplateView):
    """View for library page."""

    template_name = "imager_images/library.html"

    def get_context_data(self):
        """Get albums and photos."""
        context = {
            'albums': Album.objects.filter(published="PU").all(),
            'photos': Photo.objects.filter(published="PU").all()
        }

        return context


class AlbumsView(TemplateView):
    """View for the publicly uploaded albums."""

    template_name = "imager_images/photos.html"

    def get_context_data(self, album_id):
        """Get album photos."""
        the_album = get_object_or_404(Album, id=album_id, published="PU")
        context = {
            'album': the_album,
            'photos': the_album.photos.all()
        }

        return context


class PhotoAdd(LoginRequiredMixin, CreateView):
    """Class based view for adding a photo."""

    template_name = "imager_images/add_new.html"
    model = Photo
    fields = [
        'image',
        'title',
        'description',
        'published'
    ]

    success_url = reverse_lazy("library")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        """Form should update the profile."""
        self.object = form.save(commit=False)
        self.object.profile = ImagerProfile.objects.get(user=self.request.user)
        self.object.save()
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

    success_url = reverse_lazy("library")
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
        'published'
    ]
    success_url = reverse_lazy("library")
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
    success_url = reverse_lazy("library")
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
