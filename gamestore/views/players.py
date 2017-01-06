from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from gamestore.models import Game, GameSale, Profile


def game_detail(request, game_id):
    """Details about the game"""
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    play = is_user_allowed_to_play(game, request)
    context = {'game': game, 'play': play, 'buy': not play}
    return render(request, "gamestore/game_description.html", context)


@login_required
def game_play(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    start_game = is_user_allowed_to_play(game, request)
    context = {'game': game, 'start_game': start_game, 'buy': not start_game}
    return render(request, "gamestore/game_description.html", context)


@login_required
def game_buy(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {'buyer': request.user, 'game': game}
    return render(request, "gamestore/game_buy.html", context)


def game_sale(request, user_id):
    games_bought = GameSale.objects.filter(buyer=user_id)
    games_published = Game.objects.filter(publisher=user_id)
    user_profile = Profile.objects.filter(user=user_id)[0]

    context = {
        'game_sales': games_bought,
        'game_uploads': games_published,
        'profile': user_profile
    }

    return render(request, "gamestore/game_sale.html", context)


@login_required
def game_like(request, game_id):
    return None


def js_test(game):
    game.url = 'http://users.metropolia.fi/~nikolaid/game/index.html'
    game.image = 'http://users.metropolia.fi/~nikolaid/game.png'


def is_user_allowed_to_play(game, request):
    play = False
    user = request.user
    if user.is_authenticated():
        sale = GameSale.objects.filter(buyer=user, game=game).count()
        play = sale > 0
    return play