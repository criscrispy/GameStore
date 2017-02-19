import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from imagefactory import create_image

from gamestore.models import Category
from gamestore.tests.create_content import create_user, \
    create_game, create_score, create_game_sale, create_category

CATEGORY_TITLES = (
    '3D', 'Action', 'Adventure', 'Alien', 'Arcade', 'Card', 'Dress Up',
    'Fantasy', 'Fighting', 'Flying', 'Football', 'Golf', 'Holidays', 'Kids',
    'Multiplayer', 'Pool', 'Puzzle', 'Racing', 'Simulation', 'Sports',
    'Strategy', 'Winter', 'Word', 'Zombie'
)


def create_users(amount):
    for _ in range(amount):
        yield create_user()


def create_games(amount, users, categories):
    image_game = create_image(name='image', width=256, height=256)
    image_icon = create_image(name='icon', width=48, height=48)
    # TODO: Better titles
    if users and categories:
        for _ in range(amount):
            yield create_game(
                random.choice(users),
                random.choice(categories),
                icon=image_icon,
                image=image_game)


def populate(user_amount, game_amount, sales_amount, scores_amount):
    categories = tuple(map(create_category, CATEGORY_TITLES))
    users = tuple(create_users(user_amount))
    games = tuple(create_games(game_amount, users, categories))
    sales = []
    sales_dict = {}

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
            create_score(*random.choice(sales))


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
    help = 'Populates database with data for testing the website.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            dest='user_amount',
            default=10,
            type=int,
            help='Amount of users to create.'
        )
        parser.add_argument(
            '--games',
            dest='game_amount',
            default=2,
            type=int,
            help='Amount of games to create.'
        )
        parser.add_argument(
            '--sales',
            dest='sales_amount',
            default=10,
            type=int,
            help='Amount of sales to create.'
        )
        parser.add_argument(
            '--scores',
            dest='scores_amount',
            default=20,
            type=int,
            help='Amount of scores to create.'
        )

    def handle(self, *args, **options):
        populate(
            options['user_amount'],
            options['game_amount'],
            options['sales_amount'],
            options['scores_amount'],
        )
