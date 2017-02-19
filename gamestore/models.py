"""Gamestore Models

Attributes:
    DEVELOPER_STATUS_CHOICES:
        - basic_user=not_developer,
        - pending=user has applied to become a developer
        - confirmed=user is a developer

    GENDER_CHOICES:
        - Other
        - Male
        - Female


References:
    Profile

    - https://stackoverflow.com/questions/6085025/django-user-profile
    - https://stackoverflow.com/questions/35030556/django-user-profile-in-1-9
    - https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/
    - https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    - http://bootsnipp.com/snippets/featured/simple-user-profile

"""
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# from django.contrib.postgres.fields import JSONField

DEVELOPER_STATUS_CHOICES = (
    (0, 'basic_user'),
    (1, 'pending'),
    (2, 'confirmed'),
)

GENDER_CHOICES = (
    ('other', 'Other'),
    ('male', 'Male'),
    ('female', 'Female'),
)

PROFILE_DEFAULT = os.path.join(
    settings.STATIC_ROOT, 'images', 'profile_default.png')
GAME_ICON_DEFAULT = os.path.join(
    settings.STATIC_ROOT, 'images', 'game_image_default.png')
GAME_IMAGE_DEFAULT = os.path.join(
    settings.STATIC_ROOT, 'images', 'game_icon_default.png')


class UserProfile(models.Model):
    """User profile.

    Image sizes

    - picture: 300x300

    Todo:
        - Picture constraints (size, ...) -> django-imagekit
        - Picture default url
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField("Profile picture", upload_to="profiles",
                                null=True, blank=True)
    gender = models.CharField(default='', max_length=140, blank=True,
                              choices=GENDER_CHOICES)
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True, max_length=500)
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)
    developer_status = models.IntegerField(default=0,
                                           choices=DEVELOPER_STATUS_CHOICES)

    def can_apply_for_developer(self):
        return int(self.developer_status) == 0

    def is_developer(self):
        """Is user a developer."""
        return int(self.developer_status) == 2

    def get_status_string(self):
        if int(self.developer_status) == 0:
            return 'Player'
        elif int(self.developer_status) == 1:
            return 'Developer application is pending'
        elif int(self.developer_status) == 2:
            return 'Developer'
        else:
            return ''

    def change_status_player(self):
        self.developer_status = 0
        self.save()

    def change_status_pending(self):
        self.developer_status = 1
        self.save()

    def change_status_developer(self):
        self.developer_status = 2
        self.save()

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create `Profile` for every `User` that is created."""
    if created:
        user_profile = UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


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
    """Model for a game added into the gamestore.

    Image sizes

    - icon:  48x48
    - image: 256x256

    Todo:
        - Unique title?
        - Price using django-money module?
        - Validate image size
    """
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField("Description of the game.", blank=False)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=False)
    price = models.DecimalField(
        "Price for the game. Value can be between 0 and 100.",
        max_digits=4, decimal_places=2, blank=False,
    )
    url = models.URLField("Game url", blank=False)
    icon = models.ImageField("Game icon", null=True, blank=True,
                             upload_to="games/icons")
    image = models.ImageField("Game image", null=True, blank=True,
                              upload_to="games/image")

    def __str__(self):
        return str(self.title)


class Score(models.Model):
    """Model for individual game score."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    score = models.PositiveIntegerField("", blank=False)
    date = models.DateTimeField("", blank=False, default=timezone.now)


class GameSale(models.Model):
    """Model for individual game sale"""
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField("Date when game was bought", blank=False,
                                default=timezone.now)


class GamePayments(models.Model):
    """Model for saving data to communicate with payment API
    :param pid: payment identifier passed to API"""
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    pid = models.CharField(max_length=30, blank=False)
    date = models.DateTimeField("Date when game was bought", blank=False,
                                default=timezone.now)


class GameSettings(models.Model):
    """Model for saving game states, settings of the game are saved as json
    string"""
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=False)
    settings = models.CharField(default="", max_length=2000)
    #settings = JSONField(default="") does not work on local sqllite


class Configuration(models.Model):
    """Model for app configuration"""
    key = models.CharField(max_length=30, blank=False)
    value = models.CharField(max_length=100, blank=False)


class Application(models.Model):
    """Developer application model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    text = models.TextField('Why you want to become a developer',
                            max_length=500, blank=False)
    date = models.DateTimeField(blank=False, default=timezone.now)
    accepted = models.NullBooleanField('NotProcesses/Accepted/Rejected',
                                       default=None, blank=False)


@receiver(post_save, sender=Application)
def handle_application(sender, instance, **kwargs):
    """Django signal for handling applications. Changes developer status
    depending on whether application is accepted or rejected."""
    if instance.accepted is not None:
        if instance.accepted:
            instance.user.userprofile.change_status_developer()
        else:
            instance.user.userprofile.change_status_player()
