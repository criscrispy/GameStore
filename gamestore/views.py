from django.shortcuts import render

# Create your views here.


def index(request):
    """
    Index page for gamestore.

    TODO:
        Get list of all games. Name, description and thumbnail should be shown
        in the home page.

    """
    context = {}
    return render(request, 'gamestore/index.html', context)


def profile(request):
    """
    User profile
    """
    context = {}
    return render(request, 'accounts/profile.html', context)
