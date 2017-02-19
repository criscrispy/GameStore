import simplejson
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from gamestore.models import UserProfile
from gamestore.service import *


def game_detail(request, game_id):
    """
    Details about the game.

    - game object
        * Title
        * Icon
        * Image
        * Description
        * Scoreboard
        *
    - Buy / Play buttons
    """
    game = get_object_or_404(Game, id=game_id)
    # TODO delete line javascript testing
    js_test(game)
    user = request.user
    play= is_user_allowed_to_play(game, user)
    edit_delete = is_user_allowed_to_edit_delete(game, user)
    scores = find_best_scores_for_game(game)
    if play:
        last_saved = find_saved_state(game_id, request)
    else:
        last_saved = False
    context = {'game': game, 'play': play, 'buy': not play, 'saved': last_saved,
               'scores': scores, 'edit_delete':edit_delete}
    return render(request, GAME_DESCRIPTION_HTML, context)


@login_required
def game_buy(request, game_id):
    """Allow player to buy a game if he has not already bought else redirect
    to game_detail."""
    game = get_object_or_404(Game, pk=game_id)
    context = load_game_buy_context(game, request)
    return render(request, GAME_BUY_HTML, context)


@login_required
def game_play(request, game_id):
    """Allow player to play a game if he has bought the game else redirect to
    game_buy."""
    context = load_game_context(game_id, request)
    return render(request, GAME_DESCRIPTION_HTML, context)


@login_required
def game_play_saved(request, game_id, last_saved):
    """Allow player to play a game from saved state"""
    context = load_game_context(game_id, request)
    if context['start_game']:
        context['last_saved'] = last_saved
    return render(request, GAME_DESCRIPTION_HTML, context)


def load_game_context(game_id, request):
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    start_game = is_user_allowed_to_play(game, request.user)
    context = {'game': game, 'start_game': start_game, 'buy': not start_game}
    return context


@login_required
def game_submit_score(request, game_id):
    """Submit score for saving"""
    score = check_received_data(request, GAME_SCORE)
    if not score:
        response = {ERROR: GAME_SCORE_INVALID}
    try:
        save_game_score(request, game_id, score)
        response = {'score': score}
    except:
        response = {ERROR: COULD_NOT_SAVE_SCORE}
    finally:
        return ajax_render_response(response)


@login_required
def game_save_settings(request, game_id):
    """Save state of the game as json"""
    state = check_received_data(request, GAME_STATE)
    if not state:
        response = {ERROR: GAME_STATE_INVALID}
    try:
        save_game_state(request, game_id, state)
        response = {'state': state}
    except:
        response = {ERROR: COULD_NOT_SAVE_STATE}
    finally:
        return ajax_render_response(response)


@login_required
def game_sale(request):
    """Games that user has bought."""
    user = request.user
    games_bought = GameSale.objects.filter(buyer=user)
    games_published = Game.objects.filter(publisher=user)
    user_profile = get_object_or_404(UserProfile, user=user)

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
    """Enable to play game from saved state"""
    try:
        state = find_saved_state(game_id, request)
        json = validate_json(state.settings, GAME_STATE)
        return game_play_saved(request, game_id, json)
    except Exception as e:
        error("game_get_saved_state", e)
        json = simplejson.dumps({'info': 'error - state not found'})
        return HttpResponse(json)


def ajax_render_response(response):
    """Render html response to ajax calls from js"""
    html = render_to_string(GAME_AJAX_HTML, response)
    return HttpResponse(html)
