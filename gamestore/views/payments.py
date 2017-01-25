"""
Selled ID: 57b91FDFa2Sy
Secret Key: 873efc3f8f8ca2605de7a4101d3322ba
API:http://payments.webcourse.niksula.hut.fi/
POST http://payments.webcourse.niksula.hut.fi/pay/
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gamestore.service import calculate_checksum, save_game_sale, validate_payment_feedback, remove_payment


@login_required
def success(request):
    """Method to be called on payment success"""
    game = validate_payment_feedback(request, 'success')
    calculate_checksum()
    save_game_sale(game, request.user)
    context = {'game': game}
    return render(request, "gamestore/payments_success.html", context)


@login_required
def cancel(request):
    """Method to be called on payment cancel"""
    message = "cancel"
    return render_payment_fail(request, message, 'cancel')


@login_required
def error(request):
    """Method to be called on payment error"""
    message = "error"
    return render_payment_fail(request, message, 'error')


def render_payment_fail(request, message, expected_result):
    game = validate_payment_feedback(request, expected_result)
    remove_payment()
    game_link = "/games/" + game.id
    context = {'message': message, 'link': game_link}
    return render(request, "gamestore/payments_fail.html", context)
