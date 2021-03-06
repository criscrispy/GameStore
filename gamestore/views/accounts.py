"""Gamestore Account Views

Profile page should display

User (auth) & UserProfile

- picture
- first_name
- last_name
- email
- gender
- website
- bio
- city
- country
- organization
- developer status

Buttons

- Apply for developer
- Edit information


Todo:
    - Display profile image
    - Allow anyone to view profiles
    - Profile edit is not redirecting correctly after submit

"""
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from gamestore.forms import UserProfileForm, UserForm, ApplicationForm
from gamestore.models import UserProfile


@login_required
def profile(request, user_id=None):
    """Show User's profile view"""
    if not user_id:
        user_id = request.user.id
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    return render(request, "accounts/profile.html", {'profile': user_profile})


@login_required
@transaction.atomic
def profile_edit(request):
    """Edit user profile information"""
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES,
                                       instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/accounts/profile/')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required()
def apply_developer(request):
    """Apply for developer status."""
    profile = request.user.userprofile

    if not profile.can_apply_for_developer():
        return redirect('/accounts/profile/')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            profile.change_status_pending()
            return redirect('/accounts/profile/')
    else:
        form = ApplicationForm()

    return render(request, 'gamestore/developer_apply.html', {
        'form': form
    })


def user_history(request, user_id):
    return HttpResponse()
