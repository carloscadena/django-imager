"""Views for displaying images and albums."""
from django.shortcuts import render
from imager_images.models import Album
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


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
        return context
