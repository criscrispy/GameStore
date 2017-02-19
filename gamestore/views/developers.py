from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect
from django.shortcuts import render

from gamestore.constants import SALE_CHART_HTML, METHOD_POST
from gamestore.forms import GameForm
from gamestore.models import Game, GameSale
from gamestore.service import validate_user, find_game_by_id, delete_game, create_chart
from gamestore.views.accounts import profile


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

    if request.method == METHOD_POST:
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
def upload_edit(request, game_id):
    """Modify existing game"""
    if not request.user.userprofile.is_developer():
        return profile(request)
    game = find_game_by_id(game_id)
    validate_user(request, game.publisher)
    return upload(request, game)


@login_required
def upload_delete(request, game_id):
    """Delete uploaded game"""
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
    return render(request, SALE_CHART_HTML, {'salechart': sale_chart})

