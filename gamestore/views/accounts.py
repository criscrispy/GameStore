from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from gamestore.models import Profile


@login_required
def profile(request):
    """User profile."""
    user_profile = get_object_or_404(Profile, user__id=request.user.id)
    context = {
        'user': request.user,
        'profile': user_profile
    }
    return render(request, "accounts/profile.html", context)


def user_history(request, user_id):
    return HttpResponse()


def apply_developer(request, user_id):
    """Apply for developer status."""
    user_profile = get_object_or_404(Profile, user__id=request.user.id)
    user_profile.developer_status = '1'
    user_profile.save()
    return profile(request)
