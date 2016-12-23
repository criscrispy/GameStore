import logging
import random
from io import BytesIO

from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker

from gamestore.models import Game, Score, GameSale, Profile
from gamestore.tests.create_content import create_image

fake = Faker()
logger = logging.getLogger(__name__)


def create_user(superuser=False):
    """

    Args:
        superuser (boolean): Create superuser

    Returns:
        User: Created user
    """
    logger.info("")

    d = dict(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password="password321"
    )

    try:
        if not superuser:
            return User.objects.create_user(**d)
        else:
            return User.objects.create_superuser(**d)
    except IntegrityError:
        # Username must be unique
        pass


def create_profile(user, image):
    """
    Create user profile.

    Args:
        user:
        image:

    Returns:

    """
    logger.info("")

    profile = Profile.objects.create(user=user)
    profile.image.save(image.name, image)
    return profile


def create_game(user, icon=None, image=None):
    """
    Create game.

    Args:
        user (User): Instance of User model.
        image (BytesIO):
        icon (BytesIO):

    Returns:
        Game: Instance of Game model.
    """
    logger.info("")

    game = Game.objects.create(
        publisher=user,
        title=fake.text(30),
        description=fake.text(),
        category=fake.text(30),
        price=fake.pyfloat(right_digits=2, positive=True),
        url=fake.url(),
    )

    # Images
    # http://www.revsys.com/blog/2014/dec/03/loading-django-files-from-code/

    if icon:
        game.icon.save(icon.name, File(icon))

    if image:
        game.image.save(image.name, File(image))

    return game


def create_score(user, game):
    """

    Args:
        game:
        user:

    Returns:

    """
    logger.info("")

    score = Score.objects.create(
        game=game,
        player=user,
        score=fake.random_int(min=0)
    )
    return score


def create_game_sale(user, game):
    """

    Args:
        user:
        game:

    Returns:

    """
    logger.info("")

    game_sale = GameSale.objects.create(
        buyer=user,
        game=game,
    )
    return game_sale


def populate(user_amount, game_amount, sales_amount, scores_amount):
    image_game = create_image("image", width=128, height=128)
    image_icon = create_image("image", width=48, height=48)
    image_profile = create_image("profile", width=128, height=128)

    users = []
    games = []
    sales = []
    sales_dict = {}

    for i in range(user_amount):
        user = create_user()
        create_profile(user, image=image_profile)  # FIXME
        users.append(user)

    if users:
        for i in range(game_amount):
            user = random.choice(users)
            game = create_game(user, icon=image_icon, image=image_game)
            games.append(game)

    if users and games:
        for i in range(sales_amount):
            user = random.choice(users)
            game = random.choice(games)

            bought = sales_dict.get(user, [])

            if not bought:
                create_game_sale(user, game)
                sales.append((user, game))
                sales_dict[user] = [game]
            elif game not in bought:
                create_game_sale(user, game)
                sales.append((user, game))
                sales_dict[user] = [game]

    if sales:
        for i in range(scores_amount):
            user, game = random.choice(sales)
            create_score(user, game)


class Command(BaseCommand):
    """
    Manage.py command for populating database with models for testing. Usage

    Populates the database with data for testing. Uses *faker* for data
    generation.

    .. code-block::

       python manage.py populate_db

    Resources:

    .. [1] http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
    """
    args = '<amount>'
    help = 'Populates database with data for testing the website.'

    def handle(self, *args, **options):
        populate(10, 10, 10, 10)
