"""Views for displaying images and albums."""
from django.shortcuts import render
from imager_images.models import Album
from imager_images.models import Photo
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from imager_profile.models import ImagerProfile
from django.http import HttpResponseRedirect
from django import forms


def library_view(request):
    """View for library page."""

    return render(request, 'imager_images/library.html')


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
        'published'
    ]

    success_url = reverse_lazy("library")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        """Form should update the profile."""
        self.object = form.save(commit=False)
        self.object.profile = ImagerProfile.objects.get(user=self.request.user)
        self.object.save()
        # form.save_m2m()
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
