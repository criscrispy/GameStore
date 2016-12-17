from django.shortcuts import render

# Create your views here.


def index(request):
    """
    Index page for gamestore.

    Args:
        request:

    Returns:

    """
    context = {}
    return render(request, 'gamestore/index.html', context)
