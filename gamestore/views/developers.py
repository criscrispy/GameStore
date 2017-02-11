from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from gamestore.forms import GameForm
from gamestore.models import Game, UserProfile
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
    """Upload new game of modify existing."""
    # if user is not a developer/publisher yet redirect to profile page where
    # they can apply
    user_profile = get_object_or_404(UserProfile, user__id=request.user.id)
    if user_profile.developer_status != '2':
        return profile(request)

    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/upload', {'status': 'success'})

    return render(request, "gamestore/upload_form.html", {'status': 'pending'})


def upload_detail(request, game_id):
    return HttpResponse()


def upload_stat(request, game_id):
    return HttpResponse()


def upload_edit(request, game_id):
    return HttpResponse()


def upload_delete(request, game_id):
    return HttpResponse()
