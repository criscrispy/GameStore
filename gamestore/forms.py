from django import forms
from gamestore.models import Game


class GameForm(forms.ModelForm):
    """
    Form for developers adding new game.
    """
    class Meta:
        model = Game
        fields = [
            'title',
            'description',
            'category',
            'price',
            'url',
            'icon',
            'image',
        ]
