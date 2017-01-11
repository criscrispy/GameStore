"""
Loading image to django model is adapted from:
http://www.revsys.com/blog/2014/dec/03/loading-django-files-from-code/
"""
import logging
import string
from functools import partial
from io import BytesIO, StringIO

from PIL import Image, ImageDraw
from django.contrib.auth.models import User
from django.core.files import File
from faker import Faker
from typing import Callable

from gamestore.models import Profile, Game, Score, GameSale, Category

BITMAP = ('jpeg', 'png', 'gif')
SVG = ('svg',)

logger = logging.getLogger(__name__)

fake = Faker()

username_alphabet = string.ascii_letters + string.digits + "@.+-_"
password_alphabet = string.ascii_letters + string.digits + string.punctuation


def _call(arg):
    """
    Call arg if it is callable otherwise return.

    Args:
        arg(object|Callable[object]):

    Returns:
        object:
    """
    if callable(arg):
        return arg()
    else:
        return arg


def _create_bitmap(name, width, height, filetype, text):
    """
    Returns:
        BytesIO:
    """
    file = BytesIO()
    file.name = name + '.' + filetype
    image = Image.new('RGBA', size=(width, height), color=(128, 128, 128))
    draw = ImageDraw.Draw(image)
    size = draw.textsize(text)
    draw.text(((width - size[0]) / 2, (height - size[1]) / 2), text)
    image.save(file, format=filetype)
    file.seek(0)
    return file


def _create_svg(name, width, height, text):
    """
    Returns:
        StringIO:
    """
    import svgwrite
    file = StringIO()
    file.name = name + '.svg'
    center = (width / 2, height / 2)
    image = svgwrite.Drawing(file.name, profile='tiny',
                             height=height, width=width)
    image.add(image.rect(insert=(0, 0), size=(width, height)))
    image.add(image.text(text, insert=center))
    image.write(file)
    file.seek(0)
    return file


def create_image(name, width=48, height=48, filetype='png', text=None):
    """
    Creates in memory images for testing.

    Args:
        name (str): Name without file extension.
        width (int): Positive integer
        height (int): Positive integer
        filetype (str): Bitmap {'jpg', 'jpeg', 'png', 'gif'}
                        Vector graphics {'svg'}
        text (str, optional): None uses default "{width}x{height}" string.
                    Otherwise supplied string is used if string is empty
                    no text is set.

    Returns:
        BytesIO|StringIO: Image as BytesIO or StringIO object.
            It can be used in same fashion as file object
            >>> file = open("image.ext", 'rb')
            created by opening a file.

    Resources:
    .. [#] http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
    .. [#] https://pillow.readthedocs.io/en/latest/
    .. [#] https://svgwrite.readthedocs.io/en/latest/overview.html
    """
    # FIXME: Text size
    # TODO: Width and height units (cm, em, px, ...)

    logging.info("")

    if text is None:
        text = "{width}x{height}".format(width=width, height=height)

    if filetype in SVG:
        return _create_svg(name, width, height, text)
    else:
        return _create_bitmap(name, width, height, filetype, text)


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
        Profile:
    """
    logger.info({'user': user, 'image': image})

    profile = Profile.objects.create(user=user)

    if image is not None:
        profile.image.save(image.name, File(image))

    return profile


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
