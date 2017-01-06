from django.http import HttpResponseRedirect
from django.shortcuts import render

from gamestore.forms import GameForm
from gamestore.models import Game, Profile
from gamestore.views.accounts import profile


def uploads(request, user_id):
    games_published = Game.objects.filter(publisher=user_id)

    context = {
        'games': games_published
    }

    return render(request, "gamestore/uploads.html", context)


def upload(request):
    # if user is not a developer/publisher, yet redirect to profile page where they can apply
    if Profile.objects.filter(user=request.user.id)[0].developer_status != '2':
        return profile(request)

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/upload', {'status': 'success'})

    return render(request, "gamestore/upload_form.html", {'status': 'pending'})


def upload_detail(request, game_id):
    return None


def upload_stat(request, game_id):
    return None


def upload_edit(request, game_id):
    return None


def upload_delete(request, game_id):
    return None