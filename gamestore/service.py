import json
import uuid
from hashlib import md5
from logging import error, debug

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from gamestore.constants import *
from gamestore.models import GameSettings, GameSale, Score, GamePayments, Game


def js_test(game):
    """URLs with game for testing"""
    game.url = 'http://users.metropolia.fi/~nikolaid/game/index.html'


def is_user_allowed_to_play(game, user):
    """
    Check if user has right to play a game, right is granted if:
    - user bought a game
    - user published a game
    """
    play = False
    if user.is_authenticated():
        sale = GameSale.objects.filter(buyer=user, game=game).count()
        dev = Game.objects.filter(publisher=user, id=game.id).count()
        play = sale > 0 or dev > 0
    return play


def find_saved_state(game_id, request):
    """Find game state provided :param game_id: for the user of request."""
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
    else:
        state = find_saved_state(game_id, request)
        if state:
            state.settings = valid_state
        else:
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
    """Check that request method is POST and if request contains :param key: return it's value."""
    if request.method == METHOD_POST:
        if key in request.POST:
            value = request.POST[key]
            return value
    return False


def find_best_scores_for_game(game, number=10):
    """Find :param number: best scores to populate scoreboard of the :param game: """
    top_scores = (Score.objects.filter(game=game)
                  .order_by('-score')
                  .values_list('score', flat=True)
                  .distinct())
    top_records = (Score.objects.filter(game=game)
                   .order_by('-score')
                   .filter(score__in=top_scores[:number]))
    return list(top_records[:number])


def load_game_buy_context(game, request):
    """Prepare context for game buying view, load parameters needed by payment API"""
    service_url = get_service_url()
    sid = get_payment_sid()
    pid = generate_pid()
    save_payment(pid, game, request.user)
    checksum = calculate_request_checksum(game, pid, sid)
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
    """Generate payment identifier"""
    uid = uuid.uuid4()
    pid = uid.hex[:8]
    return pid


def calculate_request_checksum(game, pid, sid):
    """Calculate checksum of payment details to pass to payment API"""
    secret_key = get_payment_secret()
    checksum_string = CHECKSUM_REQUEST_FORMAT.format(pid, sid, game.price, secret_key)
    return calculate_checksum(checksum_string)


def calculate_response_checksum(pid, ref, result):
    """Calculate checksum of payment details returned from payment API"""
    secret_key = get_payment_secret()
    checksum_string = CHECKSUM_RESPONSE_FORMAT.format(pid, ref, result, secret_key)
    return calculate_checksum(checksum_string)


def calculate_checksum(checksum_string):
    """Calculate md5 hex"""
    m = md5(checksum_string.encode(ASCII))
    checksum = m.hexdigest()
    return checksum


def validate_payment_feedback(request, expected_result):
    """Validate feedback received from payment API"""
    pid, checksum, ref = validate_payment_feedback_parameters(request, expected_result)
    record = find_payment_by_pid(pid)
    validate_user(request, record.buyer)
    checksum_new = calculate_response_checksum(pid, ref, expected_result)
    if checksum == checksum_new:
        return record.game, pid
    else:
        raise ValidationError(CHECKSUM_WRONG)


def validate_payment_feedback_parameters(request, expected_result):
    """Validate that all needed payment feedback parameters are present in GET request and satisfy expected format"""
    if request.method != METHOD_GET:
        return ValidationError(GET_REQUEST_EXPECTED)
    pid = request.GET[PID]
    if not pid or not pid.isalnum() or len(pid) != PID_LENGHT:
        raise ValidationError(PID_INVALID_FORMAT)
    result = request.GET[RESULT]
    if not result or result != expected_result:
        raise ValidationError(RESULT_INVALID_FORMAT)
    checksum = request.GET[CHECKSUM]
    if not checksum or not checksum.isalnum() or len(checksum) != CHECKSUM_LENGHT:
        raise ValidationError(CHECKSUM_INVALID_FORMAT)
    ref = request.GET[REF]
    if not ref or not ref.isalnum():
        raise ValidationError(REF_INVALID_FORMAT)
    return pid, checksum, ref


def find_payment_by_pid(pid):
    """Find payment details entry by payment identifier"""
    try:
        p = GamePayments.objects.get(pid=pid)
    except ObjectDoesNotExist:
        error("No payment were found with pid: %s" % pid)
        raise ValidationError(PID_WAS_NOT_FOUND)
    else:
        return p


def validate_user(request, user):
    """Make sure that request user and :param user: are same user"""
    if request.user.id != user.id or request.user.username != user.username:
        raise ValidationError(USER_INVALID)


def remove_payment(game, user, pid):
    try:
        payment = GamePayments.objects.get(game=game, pid=pid, buyer=user)
    except ObjectDoesNotExist:
        debug("No payment were found with pid: %s and user: %s" % (pid, user.username))
    else:
        payment.delete()


def find_saved_payment(game, user):
    payment = GamePayments.objects.get(game=game, buyer=user)

    return payment


def save_payment(pid, game, user):
    """Create and save or update payment entry. """
    try:
        record = find_saved_payment(game, user)
        record.pid = pid
    except ObjectDoesNotExist:
        debug("creating new game payment object")
        record = GamePayments(pid=pid, game=game, buyer=user)
    record.save()


def save_game_sale(user, game):
    """Save entry game sold"""
    game_sale = GameSale(buyer=user, game=game)
    game_sale.save()


# TODO implement configuration

def get_payment_sid():
    """Get payment sid from configuration"""
    return '57b91FDFa2Sy'


def get_payment_secret():
    """Get payment password from configuration"""
    return '873efc3f8f8ca2605de7a4101d3322ba'


def get_service_url():
    """Get game service URL from configuration"""
    return 'http://localhost:8000'
