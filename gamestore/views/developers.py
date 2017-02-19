from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from gamestore.forms import GameForm
from gamestore.models import Game, GameSale
from gamestore.service import validate_user, GAME_INVALID
from gamestore.views.accounts import profile
from chartit import DataPool, Chart


def uploads(request, user_id):
    """Uploads"""
    games_published = Game.objects.filter(publisher=user_id)
    context = {
        'games': games_published
    }
    return render(request, 'gamestore/uploads.html', context)


@login_required
def upload(request, instance = None):
    """Upload new game of modify existing.

    - Let developers add new games.
    - Redirect non developers to request developer status.

    Todo:
        - publisher: request.user
        - modify existing game
    """
    if not request.user.userprofile.is_developer():
        return profile(request, request.user.id)

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)

        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.publisher = request.user
            new_game.save()
            return HttpResponseRedirect('/games/user')
    else:
        form = GameForm(instance=instance)

    return render(request, "gamestore/upload_game.html", {'form': form})

@login_required
def upload_detail(request, game_id):

    return HttpResponse()

@login_required
def upload_edit(request, game_id):
    if not request.user.userprofile.is_developer():
        return profile(request)
    game = find_game_by_id(game_id)
    validate_user(request, game.publisher)
    return upload(request, game)


def find_game_by_id(game_id):
    try:
        game = Game.objects.get(id=game_id)
    except ObjectDoesNotExist:
        raise ValidationError(GAME_INVALID)
    return game


def delete_game(game):
    Game.objects.delete(game)



@login_required
def upload_delete(request, game_id):
    if not request.user.userprofile.is_developer():
        return profile(request)
    game = find_game_by_id(game_id)
    validate_user(request, game.publisher)
    delete_game(game)
    return render(request, "gamestore/upload_game_deleted.html", {'game': game})


@login_required
def sale_stat(request):
    '''
    Display chart with sale statistics for developer.
    Calculate amount of sold games and profit.
    '''
    if not request.user.userprofile.is_developer():
        return profile(request)
    user = request.user
    # query amount and profit
    sale = GameSale.objects.filter(game__publisher=user).annotate(date_no_time=TruncDate('date')).values('date_no_time').annotate(
        amount=Count('date_no_time')).annotate(profit=Sum('game__price'))
    if sale:
        sale_chart = create_chart(sale)
    else:
        sale_chart = False
    # Step 3: Send the chart object to the template.
    return render(request, "gamestore/sale_chart.html", {'salechart': sale_chart})


def create_chart(sale):
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
