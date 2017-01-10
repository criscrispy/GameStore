from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from gamestore.models import Game, GameSale, Profile


def game_detail(request, game_id):
    """
    Details about the game.

    - game object
        * Title
        * Icon
        * Image
        * Description
        * ...
    - Buy / Play buttons
    """
    game = get_object_or_404(Game, id=game_id)
    # TODO delete line javascript testing
    js_test(game)

    # play = is_user_allowed_to_play(game, request)
    if request.user.is_authenticated():
        sale = GameSale.objects.filter(buyer=request.user, game=game).count()
        allowed_to_play = sale > 0
    else:
        allowed_to_play = False

    context = {
        'game': game,
        'play': allowed_to_play,
        'buy': not allowed_to_play,
    }
    return render(request, "gamestore/game_description.html", context)


@login_required
def game_buy(request, game_id):
    """Allow player to buy a game if he has not already bought else redirect
    to game_play."""
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'buyer': request.user,
        'game': game
    }
    return render(request, "gamestore/game_buy.html", context)


@login_required
def game_play(request, game_id):
    """Allow player to play a game if he has bought the game else redirect to
    game_buy."""
    game = get_object_or_404(Game, id=game_id)
    # TODO delete line javascript testing
    js_test(game)

    if request.user.is_authenticated():
        sale = GameSale.objects.filter(buyer=request.user, game=game).count()
        allowed_to_play = sale > 0
    else:
        allowed_to_play = False

    context = {
        'game': game,
        'start_game': allowed_to_play,
        'buy': not allowed_to_play,
    }

    return render(request, "gamestore/game_description.html", context)


@login_required
def game_sale(request, user_id):
    """Games that user has bought."""
    # FIXME: If user is logged in there is no need for user_id in request
    games_bought = GameSale.objects.filter(buyer=user_id)
    games_published = Game.objects.filter(publisher=user_id)
    user_profile = get_object_or_404(Profile, user__id=user_id)

    context = {
        'game_sales': games_bought,
        'game_uploads': games_published,
        'profile': user_profile
    }

    return render(request, "gamestore/game_sale.html", context)


@login_required
def game_like(request, game_id):
    # TODO: This might be redundant
    return HttpResponse()


def js_test(game):
    game.url = 'http://users.metropolia.fi/~nikolaid/game/index.html'
    game.image = 'http://users.metropolia.fi/~nikolaid/game.png'
