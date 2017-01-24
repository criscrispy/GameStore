from logging import log, error, debug

from gamestore.models import GameSettings, GameSale, Score
import json
from django.core.exceptions import ObjectDoesNotExist

COULD_NOT_SAVE_SCORE = "Error: Could not save score"
COULD_NOT_SAVE_STATE = "Error: Could not save state"


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
    try:
        state = GameSettings.objects.get(game_id=game_id, player=request.user)
    except ObjectDoesNotExist:
        state = False
    return state


def validate_json(state,string=False):
    # Todo escape javascript validate json

    val_state = json.loads(state)
    if string:
        val_state = {string:val_state}
    return json.dumps(val_state)


def save_game_state(request, game_id, state):
    try:
        valid_state = validate_json(state)
    except ValueError:
        error(COULD_NOT_SAVE_STATE)
    try:
        state = find_saved_state(game_id, request)
        state.settings = valid_state
    except ObjectDoesNotExist:
        debug("creating new game state object")
        state = GameSettings(game_id=game_id, player=request.user, settings=valid_state)
    state.save()


def save_game_score(request, game_id, score):
    try:
        int_score = int(score)
        s = Score(game_id=game_id, player=request.user, score=int_score)
        s.save()
    except ValueError:
        error(COULD_NOT_SAVE_SCORE)


def check_received_data(request, key):
    if request.method == 'POST':
        if key in request.POST:
            value = request.POST[key]
            return value
    return False


def find_best_scores_for_game(game):
    top_scores = (Score.objects.filter(game=game)
                  .order_by('-score')
                  .values_list('score', flat=True)
                  .distinct())
    top_records = (Score.objects.filter(game=game)
                   .order_by('-score')
                   .filter(score__in=top_scores[:10]))
    return list(top_records[:10])

