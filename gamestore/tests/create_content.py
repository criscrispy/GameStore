"""Create fake content for testing the django application

Loading image to django model is adapted from:
http://www.revsys.com/blog/2014/dec/03/loading-django-files-from-code/

Attributes:
    USERNAME_ALPHABET:
    PASSWORD_ALPHABET:

"""
import functools
import inspect
import logging
import string
from functools import partial

from django.contrib.auth.models import User
from django.core.files import File
from faker import Faker

from gamestore.models import UserProfile, Game, Score, GameSale, Category

USERNAME_ALPHABET = string.ascii_letters + string.digits + "@.+-_"
PASSWORD_ALPHABET = string.ascii_letters + string.digits + string.punctuation
PASSWORD = "password"

logger = logging.getLogger(__name__)
fake = Faker()


class log_with(object):
    """Logging decorator that allows you to log with a specific logger.

    Todo:
        - loglevel
        - Pretty formatting
        - function call stack level
        - timer
        - args & kwargs
    """

    def __init__(self, logger=None, entry_msg=None, exit_msg=None):
        self.logger = logger
        self.entry_msg = entry_msg
        self.exit_msg = exit_msg

    def __call__(self, function):
        """Returns a wrapper that wraps func. The wrapper will log the entry
        and exit points of the function with logging.INFO level.
        """
        if not self.logger:
            # If logger is not set, set module's logger.
            self.logger = logging.getLogger(function.__module__)

        # Function signature
        sig = inspect.signature(function)
        arg_names = sig.parameters.keys()

        def message(args, kwargs):
            for i, name in enumerate(arg_names):
                try:
                    value = args[i]
                except IndexError:
                    # FIXME: Default values in kwargs
                    try:
                        value = kwargs[name]
                    except KeyError:
                        continue
                yield str(name) + ': ' + str(value)

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            self.logger.info('<' + function.__name__ + '>' + '\n' +
                             '\n'.join(message(args, kwargs)))
            result = function(*args, **kwargs)
            return result
        return wrapper


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
    category = Category.objects.create(
        title=_call(category_title),
        description=_call(description),
    )
    return category


@log_with(logger)
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
