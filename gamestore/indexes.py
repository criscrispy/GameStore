from haystack import indexes
from gamestore.models import Game


class GameIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index for searching games.

    - game.title
    - publisher.username
    - category.title
    """
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    publisher = indexes.CharField(model_attr='publisher__username')
    category = indexes.CharField(model_attr='category__title')

    def get_model(self):
        return Game

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
