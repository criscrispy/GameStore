import pytest
from django.core.exceptions import ValidationError
from django.test import RequestFactory

from hypothesis import settings

from gamestore.models import GameSettings
from gamestore.service import is_user_allowed_to_play, save_game_state, validate_payment_feedback, \
    validate_payment_feedback_parameters, PID_INVALID_FORMAT, REQUEST_PARAMETER_MISSING, CHECKSUM_INVALID_FORMAT, \
    REF_INVALID_FORMAT, RESULT_INVALID_FORMAT
from gamestore.tests.create_content import create_user, create_game, create_game_sale, create_category

VALID_REF = "abc"
INVALID_REF = "\$\$"
INVALID_PID = "dsfdsf"
VALID_CHECKSUM = "12345678901234567890123456789012"
SUCCESS = "success"
VALID_PID = "12344234"

settings.register_profile('dev', settings(max_examples=10))
settings.load_profile('dev')


@pytest.mark.django_db
def test_is_user_allowed_to_play():
    game, user = create_user_game()
    result = is_user_allowed_to_play(game, user)
    assert result is False

    sale = create_game_sale(user, game)
    result = is_user_allowed_to_play(game, user)
    assert result

    dev_user = game.publisher
    result = is_user_allowed_to_play(game, dev_user)
    assert result


def create_user_game():
    user = create_user()
    dev_user = create_user()
    category = create_category("a", "b")
    game = create_game(dev_user, category)
    return game, user


@pytest.mark.django_db
def test_save_game_state_saved_once():
    game, user = create_user_game()
    state1 = "{\"width\": 500, \"height\": 500}"
    state2 = "{\"dsads\":{}}"
    state3 = "{\"erwe4454\": {}}"
    request_factory = RequestFactory()
    request = request_factory.get("")
    request.user = user
    save_game_state(request, game.id, state1)
    save_game_state(request, game.id, state2)
    save_game_state(request, game.id, state3)
    result = GameSettings.objects.filter(game=game, player=user)
    assert result.count() == 1
    state = result.first()
    assert state.settings == state3


@pytest.mark.django_db
def test_validate_payment_feedback():
    request_factory = RequestFactory()

    data = {'pid': INVALID_PID, 'result': SUCCESS, 'checksum': "", 'ref': ""}
    request = request_factory.get("", data)
    request.user = create_user()
    try:
        validate_payment_feedback_parameters(request, SUCCESS)
        assert False
    except ValidationError as e:
        assert e.message == PID_INVALID_FORMAT

    data = {'pid': VALID_PID, 'result': SUCCESS, 'ref': ""}
    request = request_factory.get("", data)
    try:
        validate_payment_feedback_parameters(request, SUCCESS)
        assert False
    except ValidationError as e:
        assert e.message == REQUEST_PARAMETER_MISSING

    data = {'pid': VALID_PID, 'result': SUCCESS, 'checksum': ""}
    request = request_factory.get("", data)
    try:
        validate_payment_feedback_parameters(request, SUCCESS)
        assert False
    except ValidationError as e:
        assert e.message == REQUEST_PARAMETER_MISSING


    data = {'pid': VALID_PID, 'result': SUCCESS, 'checksum': "", 'ref': ""}
    request = request_factory.get("", data)
    request.user = create_user()
    try:
        validate_payment_feedback_parameters(request, SUCCESS)
        assert False
    except ValidationError as e:
        assert e.message == CHECKSUM_INVALID_FORMAT

    data = {'pid': VALID_PID, 'result': SUCCESS, 'checksum': VALID_CHECKSUM, 'ref': INVALID_REF}
    request = request_factory.get("", data)
    request.user = create_user()
    try:
        validate_payment_feedback_parameters(request, SUCCESS)
        assert False
    except ValidationError as e:
        assert e.message == REF_INVALID_FORMAT

    data = {'pid': VALID_PID, 'result': "cancel", 'checksum': VALID_CHECKSUM, 'ref': VALID_REF}
    request = request_factory.get("", data)
    request.user = create_user()
    try:
        validate_payment_feedback_parameters(request, SUCCESS)
        assert False
    except ValidationError as e:
        assert e.message == RESULT_INVALID_FORMAT

    data = {'pid': VALID_PID, 'result': SUCCESS, 'checksum': VALID_CHECKSUM, 'ref': VALID_REF}
    request = request_factory.get("", data)
    request.user = create_user()
    pid, checksum, ref = validate_payment_feedback_parameters(request, SUCCESS)
    assert pid==VALID_PID
    assert checksum == VALID_CHECKSUM
    assert ref == VALID_REF
