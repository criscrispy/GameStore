"""Base views

Todo:
    Pagination
"""
import logging

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from gamestore.models import Game, Category, User
from django.db.models import Q

logger = logging.getLogger(__name__)


def index(request):
    """
    Index page for gamestore.

    Args:
        request (HttpRequest):

    Returns:
        HttpResponse:
    """
    # return render(request, 'gamestore/index.html', {})
    return games(request)


def games(request):
    """Search and display games

    Searchable fields

    - game.title
    - game.publisher.username
    - game.category.title

    This is very simple implementation of search, but not very scalable. Sould
    be replaced with whoosh or elasticsearch for bigger apps.

    References:
        http://stackoverflow.com/questions/2584502/simple-search-in-django

    Todo:
        - Order the results by something
        - Search by category
        - Games in the category
        - Search by publisher
        - Games by publisher
    """
    query = request.GET.get('q')
    if query:
        games = Game.objects.filter(
            Q(title__icontains=query) |
            Q(publisher__username__icontains=query) |
            Q(category__title__icontains=query)
        )
    else:
        games = Game.objects.all()[:50]

    return render(request, "gamestore/games.html", {'games': games})
