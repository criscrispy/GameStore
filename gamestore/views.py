import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Get an instance of a logger
logger = logging.getLogger('gamestore.views')


def index(request):
    """
    Index page for gamestore.

    TODO:
        Get list of all games. Name, description and thumbnail should be shown
        in the home page.

    """
    context = {}
    return render(request, 'gamestore/index.html', context)


@login_required
def profile(request):
    """
    User profile.
    https://stackoverflow.com/questions/9046533/creating-user-profile-pages-in-django
    """
    context = {}
    return render(request, 'accounts/profile.html', context)
