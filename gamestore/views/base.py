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


def categories(request):
    """Show all categories."""
    context = {'categories': Category.objects.all()[:50]}
    return render(request, "gamestore/categories.html", context)


def category_detail(request, category_name):
    """Show all games under some category."""
    category = Category.objects.filter(title=category_name)
    games_in_category = Game.objects.filter(category_id=category)

    context = {
        'category_name': category_name,
        'games': games_in_category
    }

    return render(request, "gamestore/category_detail.html", context)


def publishers(request):
    """Show all publishers"""
    publishers_list = User.objects.filter(userprofile__developer_status=2)

    context = {
        'publishers': publishers_list
    }

    return render(request, "gamestore/publishers.html", context)


def publisher_detail(request, user_id):
    """Show all games under some publisher."""
    publishers_games = Game.objects.filter(publisher=user_id)
    context = {
        'games': publishers_games,
        'user': request.user
    }

    return render(request, "gamestore/publisher_detail.html", context)
