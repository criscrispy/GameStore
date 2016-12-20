from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class UserProfile(models.Model):
    """
    User profile.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    image = models.ImageField("Profile image.", upload_to="profile")


class Game(models.Model):
    """
    Model for a game added into the gamestore.
    """
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField("Description of the game.", blank=False)
    # TODO: category choices
    category = models.CharField(max_length=30, default="miscellaneous")
    price = models.FloatField(
        "Price for the game. "
        "Value must be greater or equal to zero.",
        blank=False,
        validators=[MinValueValidator(0.0, "Value must be positive.")]
    )
    url = models.URLField("", blank=False)
    icon = models.ImageField("", upload_to="games")
    image = models.ImageField("", upload_to="games")


class Score(models.Model):
    """
    Model for individual game score.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    score = models.PositiveIntegerField("", blank=False)
    # public = models.BooleanField(blank=False)


class GameSale(models.Model):
    """
    Model for individual game sale
    """
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    date = models.DateField("Date when game was bought", blank=False)
