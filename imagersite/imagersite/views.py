"""Views for the home page."""
from django.shortcuts import render


def home_view(request):
    """View for home page."""
    context = {'stuff': 'somestuff'}
    return render(request, 'imagersite/home.html', context=context)
