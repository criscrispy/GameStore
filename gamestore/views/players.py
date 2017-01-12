import json

import simplejson
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from gamestore.models import Game, GameSale, Profile, GameSettings, Score

COULD_NOT_SAVE_SCORE = "Error: Could not save score"
COULD_NOT_SAVE_STATE = "Error: Could not save state"


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
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    user = request.user
    play = is_user_allowed_to_play(game, user)
    try:
        last_saved = find_saved_state(game_id, request)
    except ObjectDoesNotExist:
        last_saved = False
    context = {'game': game, 'play': play, 'buy': not play, 'saved': last_saved}
    return render(request, "gamestore/game_description.html", context)


@login_required
def game_buy(request, game_id):
    """Allow player to buy a game if he has not already bought else redirect
    to game_detail."""
    game = get_object_or_404(Game, pk=game_id)
    context = {'buyer': request.user, 'game': game}
    return render(request, "gamestore/game_buy.html", context)


@login_required
def game_play(request, game_id):
    """Allow player to play a game if he has bought the game else redirect to
    game_buy."""
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    start_game = is_user_allowed_to_play(game, request.user)
    context = {'game': game, 'start_game': start_game, 'buy': not start_game}
    return render(request, "gamestore/game_description.html", context)


@login_required
def game_submit_score(request, game_id):
    """Submit score for saving"""
    score = check_received_data(request, 'gameScore')
    if score:
        save_game_score(request, game_id, score)
    return game_detail(request, game_id)


@login_required
def game_save_settings(request, game_id):
    state = check_received_data(request, 'gameState')
    if state:
        save_game_state(request, game_id, state)
    return game_detail(request, game_id)


@login_required
def game_sale(request, user_id):
    """Games that user has bought."""
    games_bought = GameSale.objects.filter(buyer=user_id)
    games_published = Game.objects.filter(publisher=user_id)
    user_profile = Profile.objects.get(user=user_id)  # TODO: exception handling

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


@login_required
def game_get_saved_state(request, game_id):
    try:
        state = find_saved_state(game_id, request)
        json = simplejson.dumps(state.settings)
        return HttpResponse(json, mimetype='application/json')
    except Exception as e:
        # todo log(e)
        json = simplejson.dumps({'info': 'error - state not found'})
        return HttpResponse(json, mimetype='application/json')


def js_test(game):
    game.url = 'http://users.metropolia.fi/~nikolaid/game/index.html'
    game.image = 'http://users.metropolia.fi/~nikolaid/game.png'


def is_user_allowed_to_play(game, user):
    play = False
    if user.is_authenticated():
        sale = GameSale.objects.filter(buyer=user, game=game).count()
        play = sale > 0
    return play


def find_saved_state(game_id, request):
    state = GameSettings.objects.get(game_id=game_id, player=request.user)
    return state


def validate_json(state):
    # Todo escape javascript validate json
    val_state = json.loads(state)
    return json.dumps(state)


def save_game_state(request, game_id, state):
    try:
        valid_state = validate_json(state)
    except ValueError:
        print(COULD_NOT_SAVE_STATE)
    try:
        state = find_saved_state(game_id, request)
        state.settings = valid_state
    except ObjectDoesNotExist:
        state = GameSettings(game_id=game_id, player=request.user, settings=valid_state)
    state.save()


def save_game_score(request, game_id, score):
    try:
        int_score = int(score)
        s = Score(game_id=game_id, player=request.user, score=int_score)
        s.save()
    except ValueError:
        print(COULD_NOT_SAVE_SCORE)


def check_received_data(request, key):
    if request.method == 'POST':
        if key in request.POST:
            value = request.POST[key]
            return value
    return False
