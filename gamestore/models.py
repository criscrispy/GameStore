from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Profile(models.Model):
    """User profile."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    image = models.ImageField("Profile image.", upload_to="profile")

    """
    developer_status enum field :
        basic_user=not_developer,
        pending=user has applied to become a developer
        confirmed=user is a developer
    """
    developer_status_choices = (
        ('0', 'basic_user'),
        ('1', 'pending'),
        ('2', 'confirmed'),
    )
    developer_status = models.CharField(max_length=1, default='0',
                                        choices=developer_status_choices)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)


class Category(models.Model):
    """Model for categories"""

    title = models.CharField(max_length=30, blank=False, unique=True)
    description = models.TextField("Description of the category.", blank=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.title)


class Game(models.Model):
    """Model for a game added into the gamestore."""
    # TODO: Unique title?
    # TODO: Price using django-money module?
    # TODO: Validate image size

    title = models.CharField(max_length=30, blank=False)
    description = models.TextField("Description of the game.", blank=False)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=False)
    price = models.DecimalField(
        "Price for the game. Value can be between 0 and 100.",
        max_digits=4, decimal_places=2, blank=False,
    )
    url = models.URLField("", blank=False)
    icon = models.ImageField("", upload_to="games")
    image = models.ImageField("", upload_to="games")


class Score(models.Model):
    """Model for individual game score."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    score = models.PositiveIntegerField("", blank=False)
    date = models.DateTimeField("", blank=False, default=timezone.now)


class GameSale(models.Model):
    """Model for individual game sale"""
    # TODO: user should only be able to buy the game once
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField("Date when game was bought", blank=False,
                                default=timezone.now)


class GameSettings(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    settings = models.CharField(default="", max_length=2000)
    # todo settings = JSONField(default="")
