"""Gamestore Forms"""
from django import forms
from django.contrib.auth.models import User

from gamestore.models import Game, UserProfile


class UserForm(forms.ModelForm):
    """User form"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    """Profile form"""

    class Meta:
        model = UserProfile
        fields = ['gender', 'picture', 'website', 'bio', 'city', 'country',
                  'organization']


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
