import json
import uuid
from hashlib import md5
from logging import error, debug

from chartit import DataPool, Chart
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404

from gamestore.constants import *
from gamestore.constants import GAME_INVALID, PAYMENT_SECRET, PAYMENT_SID
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
        play = sale > 0 or is_user_allowed_to_edit_delete(game,user)
    return play

def is_user_allowed_to_edit_delete(game, user):
    edit_delete = False
    if user.is_authenticated():
        dev = Game.objects.filter(publisher=user, id=game.id).count()
        edit_delete = dev > 0
    return edit_delete

def find_saved_state(game_id, request):
    """Find game state provided :param game_id: for the user of request."""
    try:
        state = GameSettings.objects.get(game_id=game_id, player=request.user)
    except ObjectDoesNotExist:
        state = False
    return state


def validate_json(state, string=False):
    """Validates json, if :param string provided json is returned in dictionary as value of string"""
    try:
        val_state = json.loads(state)
    except ValueError:
        error(NOT_A_VALID_JSON)
        raise ValidationError(NOT_A_VALID_JSON)
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
    service_url = get_service_url(request)
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
    try:
        pid = request.GET[PID]
        result = request.GET[RESULT]
        checksum = request.GET[CHECKSUM]
        ref = request.GET[REF]
    except KeyError:
        raise ValidationError(REQUEST_PARAMETER_MISSING)

    if not pid or not pid.isalnum() or len(pid) != PID_LENGHT:
        raise ValidationError(PID_INVALID_FORMAT)

    if not result or result != expected_result:
        raise ValidationError(RESULT_INVALID_FORMAT)

    if not checksum or not checksum.isalnum() or len(checksum) != CHECKSUM_LENGHT:
        raise ValidationError(CHECKSUM_INVALID_FORMAT)

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
    """
    Removing payment details after finished transaction. If details not found error ignored.
    """
    try:
        payment = GamePayments.objects.get(game=game, pid=pid, buyer=user)
    except ObjectDoesNotExist:
        debug("No payment were found with pid: %s and user: %s" % (pid, user.username))
    else:
        payment.delete()


def find_saved_payment(game, user):
    """
    Finding payment details ObjectDoesNotExist exception should be handled outside this method.
    """
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


def get_payment_sid():
    """Get payment sid from configuration"""
    return PAYMENT_SID


def get_payment_secret():
    """ Get payment password from configuration"""
    return PAYMENT_SECRET


def get_service_url(request):
    """Get game service URL from request"""
    url = get_current_site(request).domain
    return 'http://' + url


def find_game_by_id(game_id):
    """Find game by id"""
    try:
        game = Game.objects.get(id=game_id)
    except ObjectDoesNotExist:
        raise ValidationError(GAME_INVALID)
    return game


def delete_game(game):
    """Delete game"""
    game.delete()


def create_chart(sale):
    """ Create chart for statistics """
    # http://chartit.shutupandship.com/docs/#how-to-create-charts
    # Step 1: Create a DataPool with the data we want to retrieve.
    sale_data = \
        DataPool(
            series=
            [{'options': {
                'source': sale},
                'terms': [
                    'amount',
                    'date_no_time',
                    'profit']}
            ])
    # Step 2: Create the Chart object
    sale_chart = Chart(
        datasource=sale_data,
        series_options=
        [{'options': {
            'type': 'line',
            'stacking': False},
            'terms': {
                'date_no_time': [
                    'amount', 'profit']
            }}],
        chart_options=
        {'title': {
            'text': 'Games bought'},
            'xAxis': {
                'title': {
                    'text': 'Date'}}})
    return sale_chart


def load_game_context(game_id, request):
    """Load game context for play"""
    game = get_object_or_404(Game, pk=game_id)
    # TODO delete line javascript testing
    js_test(game)
    start_game = is_user_allowed_to_play(game, request.user)
    context = {'game': game, 'start_game': start_game, 'buy': not start_game}
    return context