from logging import log, error, debug

from gamestore.models import GameSettings, GameSale, Score, GamePayments
import json
from django.core.exceptions import ObjectDoesNotExist
import uuid
from hashlib import md5
COULD_NOT_SAVE_SCORE = "Error: Could not save score"
COULD_NOT_SAVE_STATE = "Error: Could not save state"


def js_test(game):
    """URLs with game for testing"""
    game.url = 'http://users.metropolia.fi/~nikolaid/game/index.html'


def is_user_allowed_to_play(game, user):
    """Check if user has right to play a game"""
    play = False
    if user.is_authenticated():
        sale = GameSale.objects.filter(buyer=user, game=game).count()
        play = sale > 0
    # TODO developer migth have right to play own game
    return play


def find_saved_state(game_id, request):
    """Find game state provided :param game_id for the user of request."""
    try:
        state = GameSettings.objects.get(game_id=game_id, player=request.user)
    except ObjectDoesNotExist:
        state = False
    return state


def validate_json(state, string=False):
    # Todo escape javascript validate json
    """Validates json, if :param string provided json is returned in dictionary as value of string"""
    val_state = json.loads(state)
    if string:
        val_state = {string: val_state}
    return json.dumps(val_state)


def save_game_state(request, game_id, state):
    """Saves game state, if a state for this game and user already saved - it will be overwritten by new value"""
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
    """Saves score of the game"""
    try:
        int_score = int(score)
        s = Score(game_id=game_id, player=request.user, score=int_score)
        s.save()
    except ValueError:
        error(COULD_NOT_SAVE_SCORE)


def check_received_data(request, key):
    """Check that request method is POST and if request contains :param key return it's value."""
    if request.method == 'POST':
        if key in request.POST:
            value = request.POST[key]
            return value
    return False


def find_best_scores_for_game(game):
    """Find 10 best scores to populate scoreboard of the :param game"""
    top_scores = (Score.objects.filter(game=game)
                  .order_by('-score')
                  .values_list('score', flat=True)
                  .distinct())
    top_records = (Score.objects.filter(game=game)
                   .order_by('-score')
                   .filter(score__in=top_scores[:10]))
    return list(top_records[:10])


def save_payment(pid, game, user):
    try:
        p = GamePayments(pid=pid, game=game, buyer=user)
        p.save()
    except Exception as e:
        error(e)


def load_game_buy_context(game, request):
    service_url = 'http://localhost:8000'
    sid = '57b91FDFa2Sy'
    pid = generate_pid()
    save_payment(pid, game, request.user)
    checksum = calculate_checksum(game, pid, sid)
    # checksum is the value that should be used in the payment request
    context = {
        'buyer': request.user,
        'game': game,
        'service_url': service_url,
        'pid': pid,
        'sid': sid,
        'checksum': checksum
    }
    return context


def generate_pid():
    uid = uuid.uuid4()
    pid = uid.hex[:6]
    return pid


def calculate_checksum(game, pid, sid):
    secret_key = '873efc3f8f8ca2605de7a4101d3322ba'
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, game.price, secret_key)
    # checksumstr is the string concatenated above
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return checksum
