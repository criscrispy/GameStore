"""
Selled ID: 57b91FDFa2Sy
Secret Key: 873efc3f8f8ca2605de7a4101d3322ba
API:http://payments.webcourse.niksula.hut.fi/
POST http://payments.webcourse.niksula.hut.fi/pay/
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gamestore.constants import PAYMENT_WAS_CANCELLED, ERROR_PERFORMING_PAYMENT, PAYMENTS_FAIL_HTML, \
    PAYMENTS_SUCCESS_HTML, ERROR, CANCEL, SUCCESS
from gamestore.service import save_game_sale, validate_payment_feedback, remove_payment


@login_required
def success(request):
    """Method to be called on payment success"""
    game, pid = validate_payment_feedback(request, SUCCESS)
    save_game_sale(game=game, user=request.user)
    remove_payment(game, request.user, pid)
    context = {'game': game}
    return render(request, PAYMENTS_SUCCESS_HTML, context)


@login_required
def cancel(request):
    """Method to be called on payment cancel"""
    result = CANCEL
    return render_payment_fail(request, PAYMENT_WAS_CANCELLED, result)


@login_required
def error(request):
    """Method to be called on payment error"""
    result = ERROR
    return render_payment_fail(request, ERROR_PERFORMING_PAYMENT, result)


def render_payment_fail(request, message, expected_result):
    """If payment returns error or cancel feedback is validated, payment entry removed"""
    game, pid = validate_payment_feedback(request, expected_result)
    remove_payment(game, request.user, pid)
    game_link = "/games/" + str(game.id)
    context = {'message': message, 'link': game_link}
    return render(request, PAYMENTS_FAIL_HTML, context)
