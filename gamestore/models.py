from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """
    User profile.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    image = models.ImageField("Profile image.", upload_to="profile")


class Category(models.Model):
    """
    Model for categories
    """

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=30, blank=False, unique=True)
    description = models.TextField("Description of the category.", blank=False)

    def __str__(self):
        return str(self.title)


class Game(models.Model):
    """
    Model for a game added into the gamestore.
    """
    # TODO: Unique title?
    # TODO: category choices
    # TODO: Price using django-money module?
    # TODO: Validate image size
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField("Description of the game.", blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    price = models.DecimalField(
        "Price for the game. Value can be between 0 and 100.",
        max_digits=4,
        decimal_places=2,
        blank=False,
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
    # TODO: timezone support for datetime field
    date = models.DateTimeField("", blank=False, default=timezone.now())


class GameSale(models.Model):
    """
    Model for individual game sale
    """
    # TODO: user should only be able to buy the game once
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    # TODO: timezone support for datetime field
    date = models.DateTimeField("Date when game was bought",
                                blank=False, default=timezone.now())
