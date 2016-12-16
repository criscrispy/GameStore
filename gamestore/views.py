from django.shortcuts import render

# Create your views here.


def index(request):
    """

    Args:
        request:

    Returns:

    """
    context = {}
    return render(request, 'gamestore/index.html', context)
