"""Create fake content for testing the django application

Loading image to django model is adapted from:
http://www.revsys.com/blog/2014/dec/03/loading-django-files-from-code/

Attributes:
    USERNAME_ALPHABET:
    PASSWORD_ALPHABET:

"""
import logging
import string
from functools import partial

from django.contrib.auth.models import User
from django.core.files import File
from faker import Faker

from gamestore.models import UserProfile, Game, Score, GameSale, Category

USERNAME_ALPHABET = string.ascii_letters + string.digits + "@.+-_"
PASSWORD_ALPHABET = string.ascii_letters + string.digits + string.punctuation

logger = logging.getLogger(__name__)
fake = Faker()


def _call(arg):
    """
    Call arg if it is callable otherwise return.

    Args:
        arg(object|callable[object]):

    Returns:
        object:
    """
    if callable(arg):
        return arg()
    else:
        return arg


def create_user(username=fake.user_name,
                first_name=fake.first_name,
                last_name=fake.last_name,
                email=fake.email,
                password="password",
                superuser=False):
    """
    Create user

    Args:
        username (str|Callable[str]):
        email (str|Callable[str]):
        password (str|Callable[str]):
        first_name (str|Callable[str]):
        last_name (str|Callable[str]):
        superuser (boolean): Create superuser

    Returns:
        User: Created user
    """
    logger.info("")

    if superuser:
        _create_user = User.objects.create_superuser
    else:
        _create_user = User.objects.create_user

    return _create_user(_call(username),
                        email=_call(email),
                        password=_call(password),
                        first_name=_call(first_name),
                        last_name=_call(last_name))


def create_profile(user, image=None):
    """
    Create user profile.

    Args:
        user (User):
        image (BytesIO, optional):

    Returns:
        UserProfile:
    """
    logger.info({'user': user, 'image': image})

    user_profile = UserProfile.objects.create(user=user)

    if image is not None:
        user_profile.picture.save(image.name, File(image))

    return user_profile


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
    logger.info("")

    category = Category.objects.create(
        title=_call(category_title),
        description=_call(description),
    )
    return category


def create_game(user, category,
                title=partial(fake.text, 30),
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
    logger.info("")

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

    return game


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
    logger.info("")

    score = Score.objects.create(
        game=game,
        player=user,
        score=_call(score)
    )
    return score


def create_game_sale(user, game):
    """

    Args:
        user (User):
        game (Game):

    Returns:
        GameSale:
    """
    logger.info("")

    game_sale = GameSale.objects.create(buyer=user, game=game)
    return game_sale
