"""Gamestore Signals"""
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from gamestore.models import UserProfile


def create_profile(sender, **kwargs):
    """Create `Profile` for every `User` that is created."""
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()

post_save.connect(create_profile, sender=User)
