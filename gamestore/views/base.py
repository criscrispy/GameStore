import logging

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from gamestore.models import Game, Category, User

logger = logging.getLogger(__name__)
# TODO: Pagination


def index(request):
    """
    Index page for gamestore.

    Args:
        request (HttpRequest):

    Returns:
        HttpResponse:
    """
    # context = {}
    # return render(request, 'gamestore/index.html', context)

    return games(request)


def games(request):
    """Display all games"""
    context = {'games': Game.objects.all()[:50]}
    return render(request, "gamestore/game.html", context)


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
    publishers_list = User.objects.filter(profile__developer_status='2')

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


def search(request, keyword):
    """
    Search for games using keyword. Searchable fields are

    - Game_title
    - Publisher
    - Category

    Args:
        request (HttpRequest):
        keyword (str):

    Returns:
        HttpResponse:
    """
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    return HttpResponse()
