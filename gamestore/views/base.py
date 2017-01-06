import logging

from django.shortcuts import render, get_object_or_404

from gamestore.models import Game, Category, Profile, User
from gamestore.views.accounts import profile

logger = logging.getLogger(__name__)


def index(request):
    """Index page for gamestore."""
    context = {}
    return render(request, 'gamestore/index.html', context)


def games(request):
    """Display games"""
    _games = Game.objects.all()[:50]
    context = {'games': _games}
    return render(request, "gamestore/game.html", context)


def categories(request):
    categories = Category.objects.all()[:50]
    context = {'categories': categories}
    return render(request, "gamestore/categories.html", context)


def category_detail(request, category_name):
    category = Category.objects.filter(title=category_name)
    games_in_category = Game.objects.filter(category_id=category)

    context = {
        'category_name': category_name,
        'games': games_in_category
    }

    return render(request, "gamestore/category_detail.html", context)


def user_history(request, user_id):
    return None


def publishers(request):
    publishers_list = User.objects.filter(profile__developer_status='2')

    context = {
        'publishers': publishers_list
    }

    return render(request, "gamestore/publishers.html", context)


def publisher_detail(request, user_id):
    publishers_games = Game.objects.filter(publisher=user_id)
    context = {
        'games': publishers_games,
        'user': request.user
    }

    return render(request, "gamestore/publisher_detail.html", context)


def apply_developer(request, user_id):
    user_profile = get_object_or_404(Profile, pk=request.user.id)
    user_profile.developer_status = '1'
    user_profile.save()
    return profile(request)


def search(request, keyword):
    return None
