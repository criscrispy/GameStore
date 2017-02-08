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

from gamestore.forms import UserProfileForm, UserForm
from gamestore.models import UserProfile


@login_required
def profile(request):
    """Show User's profile view"""
    user_profile = get_object_or_404(UserProfile, user__id=request.user.id)
    context = {
        'user': request.user,
        'profile': user_profile
    }
    return render(request, "accounts/profile.html", context)


@login_required
@transaction.atomic
def profile_edit(request):
    """Edit user profile information"""
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST,
                                       instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            # Update was successful
            user_form.save()
            profile_form.save()
            return redirect("/accounts/profile/")
        else:
            # Error
            pass
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
    # TODO: replace with better implementation
    user_profile = get_object_or_404(UserProfile, user__id=request.user.id)
    user_profile.developer_status = '1'
    user_profile.save()
    return profile(request)


def user_history(request, user_id):
    return HttpResponse()
