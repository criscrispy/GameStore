"""Create fake content for testing the django application

Loading image to django model is adapted from:
http://www.revsys.com/blog/2014/dec/03/loading-django-files-from-code/

Attributes:
    USERNAME_ALPHABET:
    PASSWORD_ALPHABET:

"""
import logging
import os
import string
from functools import partial

from django.contrib.auth.models import User
from django.core.files import File
from django.db.utils import IntegrityError
from faker import Faker

from gamestore.models import UserProfile, Game, Score, GameSale, Category
from gamestore.utils import log_with

USERNAME_ALPHABET = string.ascii_letters + string.digits + "@.+-_"
PASSWORD_ALPHABET = string.ascii_letters + string.digits + string.punctuation
PASSWORD = "password"
BASE_DIR = os.path.dirname(__file__)


with open(os.path.join(BASE_DIR, 'category_titles.txt')) as file:
    CATEGORY_TITLES = file.read().split('\n')

with open(os.path.join(BASE_DIR, 'game_titles.txt')) as file:
    GAME_TITLES = file.read().split('\n')


# Faker instance for creating fake data.
fake = Faker()
logger = logging.getLogger(__name__)


def _call(arg):
    """Call arg if it is callable otherwise return."""
    return arg() if callable(arg) else arg


@log_with(logger)
def create_user(username=fake.user_name,
                first_name=fake.first_name,
                last_name=fake.last_name,
                email=fake.email,
                password=PASSWORD,
                picture=None,
                superuser=False):
    """Create new user. UserProfile by django signals by default.

    Args:
        username (str|Callable[str]):
        email (str|Callable[str]):
        password (str|Callable[str]):
        first_name (str|Callable[str]):
        last_name (str|Callable[str]):
        superuser (boolean): Create superuser
        picture (BytesIO, optional):

    Returns:
        User: Created user
    """
    try:
        if superuser:
            _create_user = User.objects.create_superuser
        else:
            _create_user = User.objects.create_user

        user = _create_user(_call(username),
                            email=_call(email),
                            password=_call(password),
                            first_name=_call(first_name),
                            last_name=_call(last_name))

        user_profile = UserProfile.objects.get(user=user)
        if picture is not None:
            user_profile.picture.save(picture.name, File(picture))
    except IntegrityError:
        user = User.objects.get(username=username)

    return user


@log_with(logger)
def create_category(category_title=fake.word,
                    description=fake.text):
    """
    Create category

    Args:
        category_title (str|Callable[str]):
        description (str|Callable[str]):

    Returns:
        Category:
    """
    try:
        category = Category.objects.create(
            title=_call(category_title),
            description=_call(description),
        )
    except IntegrityError:
        category = Category.objects.get(title=category_title)

    return category


@log_with(logger)
def create_game(user, category,
                title=fake.word,
                description=fake.text,
                price=partial(fake.pydecimal, 2, 2, True),
                url=fake.url,
                icon=None,
                image=None):
    """
    Create game.

    Args:
        user (User):
            Instance of User model.

        category (Category):

        title (str|Callable[str]):
            String of max length 30.

        description (str|Callable[str]):

        price (Decimal|Callable[Decimal]):
            Positive decimal number with 2 right digits and 2 left digits.

        url (str|Callable[str]):
        image (BytesIO, optional):
        icon (BytesIO, optional):

    Returns:
        Game: Instance of Game model.
    """
    try:
        game = Game.objects.create(
            publisher=_call(user),
            category=_call(category),
            title=_call(title),
            description=_call(description),
            price=_call(price),
            url=_call(url),
        )

        if icon:
            game.icon.save(icon.name, File(icon))

        if image:
            game.image.save(image.name, File(image))
    except IntegrityError:
        game = Game.objects.get(title=title)

    return game


@log_with(logger)
def create_score(user, game,
                 score=partial(fake.random_int, min=0)):
    """

    Args:
        user (User):
        game (Game):
        score (int|Callable[int]):

    Returns:
        Score:
    """
    score = Score.objects.create(
        game=game,
        player=user,
        score=_call(score)
    )
    return score


@log_with(logger)
def create_game_sale(user, game):
    """

    Args:
        user (User):
        game (Game):

    Returns:
        GameSale:
    """
    game_sale = GameSale.objects.create(buyer=user, game=game)
    return game_sale
