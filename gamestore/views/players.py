import simplejson
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from gamestore.models import Game, Profile
from gamestore.service import *


def game_detail(request, game_id):
    """
    Details about the game.

    - game object
        * Title
        * Icon
        * Image
        * Description
        * ...
        * highscores
    - Buy / Play buttons
    """
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    user = request.user
    play = is_user_allowed_to_play(game, user)
    scores = find_best_scores_for_game(game)
    if play:
        last_saved = find_saved_state(game_id, request)
    else:
        last_saved = False
    context = {'game': game, 'play': play, 'buy': not play, 'saved': last_saved, 'scores': scores}
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
    if not score:
        response = {'error':"Error: score received from the game invalid"}
    try:
        save_game_score(request, game_id, score)
        response = {'score': score}
    except:
        response = {'error':"Error: could not save score"}
    finally:
        return ajax_render_response(response)

@login_required
def game_save_settings(request, game_id):
    state = check_received_data(request, 'gameState')
    if not state:
        response = {'error': "Error: state received from the game invalid"}
    try:
        save_game_state(request, game_id, state)
        response = {'state': state}
    except:
        response = {'error': "Error: could not save state"}
    finally:
        return ajax_render_response(response)



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
        json = validate_json(state.settings,'gameState')
        return HttpResponse(json)
    except Exception as e:
        error("game_get_saved_state", e)
        json = simplejson.dumps({'info': 'error - state not found'})
        return HttpResponse(json)



def ajax_render_response(response):
    html = render_to_string('gamestore/game_ajax.html', response)
    return HttpResponse(html)
