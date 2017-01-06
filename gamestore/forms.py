from django import forms
from gamestore.models import Game


class ProfileForm:
    pass


class GameForm(forms.ModelForm):
    """Form for developers uploading a new game or modifying information."""
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
