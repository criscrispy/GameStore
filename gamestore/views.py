import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from gamestore.models import Game, Category, GameSale

logger = logging.getLogger(__name__)


def index(request):
    """Index page for gamestore."""
    context = {}
    return render(request, 'gamestore/index.html', context)


@login_required
def profile(request):
    """User profile."""
    # TODO: https://stackoverflow.com/questions/9046533/creating-user-profile-pages-in-django
    context = {}
    return render(request, 'accounts/profile.html', context)


def games(request):
    """Display games"""
    games = Game.objects.all()[:50]
    context = {'games': games}
    return render(request, "gamestore/game.html", context)


def game_detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete 2 lines javascript testing
    game.url = 'http://users.metropolia.fi/~nikolaid/game/index.html'
    game.image = 'http://users.metropolia.fi/~nikolaid/game.png'
    # TODO add logic to control if user is allowed to play or buy
    play = True
    buy = False
    return render(request, "gamestore/game_description.html",
                  {'game': game, 'play': play, 'buy': buy})


def game_play(request, game_id):
    # TODO check user is allowed to play
    game = get_object_or_404(Game, pk=game_id)
    return render(request, "gamestore/game_description.html",
                  {'game': game, 'start_game': True})


def game_buy(request, game_id):
    return None


def game_like(request, game_id):
    return None


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


def game_sale(request, user_id):
    games_bought = GameSale.objects.filter(buyer=user_id)
    games_published = Game.objects.filter(publisher=user_id)

    context = {
        'game_sales': games_bought,
        'game_uploads': games_published
    }

    return render(request, "gamestore/game_sale.html", context)


def user_history(request, user_id):
    return None


def uploads(request, user_id):
    games_published = Game.objects.filter(publisher=user_id)

    context = {
        'games': games_published
    }

    return render(request, "gamestore/uploads.html", context)


def upload(request):
    return None


def upload_detail(request, game_id):
    return None


def upload_stat(request, game_id):
    return None


def upload_edit(request, game_id):
    return None


def upload_delete(request, game_id):
    return None


def publishers(request):
    return render(request, "gamestore/publishers.html", {})


def publisher_detail(request, user_id):
    publisher = {
        'user_id': user_id
    }

    return render(request, "gamestore/publisher_detail.html",
                  {'publisher': publisher})


def search(request, keyword):
    return None
