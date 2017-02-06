"""Gamestore Account Views"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from gamestore.forms import UserProfileForm
from gamestore.models import UserProfile


@login_required
def profile(request):
    """User profile view.

    - Show user profile
    - Change user profile

    Todo:
        - Display profile image

    """
    user_profile = get_object_or_404(UserProfile, user__id=request.user.id)
    context = {
        'user': request.user,
        'profile': user_profile
    }
    return render(request, "accounts/profile.html", context)


@login_required
def edit_user(request, pk):
    """Edit User Information"""
    user = User.objects.get(pk=pk)
    user_form = UserProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(
        User, UserProfile,
        fields=('website', 'bio', 'city', 'country', 'organization')
    )
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(request.POST, request.FILES,
                                        instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES,
                                           instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES,
                                               instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "account/account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied()


def user_history(request, user_id):
    return HttpResponse()


def apply_developer(request, user_id):
    """Apply for developer status."""
    user_profile = get_object_or_404(UserProfile, user__id=request.user.id)
    user_profile.developer_status = '1'
    user_profile.save()
    return profile(request)
