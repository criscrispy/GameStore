from django.shortcuts import render
from haystack.query import SearchQuerySet


def search(request):
    """Search for games using keyword. Searchable fields are

    - game.title
    - game.publisher
    - game.category

    """
    # FIXME:
    games_query = SearchQuerySet().autocomplete(
        content_auto=request.POST.get('search_text', '')
    )
    context = {'query': games_query}
    return render(request, 'gamestore/search.html', context)
