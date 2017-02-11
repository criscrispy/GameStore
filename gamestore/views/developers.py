from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from gamestore.forms import GameForm
from gamestore.models import Game
from gamestore.views.accounts import profile


def uploads(request, user_id):
    """Uploads"""
    games_published = Game.objects.filter(publisher=user_id)
    context = {
        'games': games_published
    }
    return render(request, 'gamestore/uploads.html', context)


@login_required
def upload(request):
    """Upload new game of modify existing.

    - Let developers add new games.
    - Redirect non developers to request developer status.

    Todo:
        - publisher: request.user
        - modify existing game
    """
    if not request.user.userprofile.is_developer():
        return profile(request)

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)

        if form.is_valid():
            new_game = form.save(commit=False)
            new_game.publisher = request.user
            new_game.save()
            return HttpResponseRedirect('/games/user')
    else:
        form = GameForm()

    return render(request, "gamestore/upload_game.html", {'form': form})


def upload_detail(request, game_id):
    return HttpResponse()


def upload_stat(request, game_id):
    return HttpResponse()


def upload_edit(request, game_id):
    return HttpResponse()


def upload_delete(request, game_id):
    return HttpResponse()
