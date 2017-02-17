import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from imagefactory import create_image

from gamestore.models import Category
from gamestore.tests.create_content import create_user, \
    create_game, create_score, create_game_sale, create_category


def create_categories(*titles):
    for title in titles:
        try:
            yield create_category(title)
        except IntegrityError:
            yield Category.objects.get(title=title)


def populate(user_amount, game_amount, sales_amount, scores_amount):
    image_game = create_image(name="image", width=256, height=256)
    image_icon = create_image(name="icon", width=48, height=48)
    category_titles = (
        '3D', 'Action', 'Adventure', 'Alien', 'Arcade', 'Card', 'Dress Up',
        'Fantasy', 'Fighting', 'Flying', 'Football', 'Golf', 'Holidays', 'Kids',
        'Multiplayer', 'Pool', 'Puzzle', 'Racing', 'Simulation', 'Sports',
        'Strategy', 'Winter', 'Word', 'Zombie'
    )

    categories = list(create_categories(*category_titles))
    users = []
    games = []
    sales = []
    sales_dict = {}

    for i in range(user_amount):
        try:
            user = create_user()
            users.append(user)
        except IntegrityError:
            # Tries to create new user with existing username
            pass

    if users and categories:
        for i in range(game_amount):
            user = random.choice(users)
            rand_category = random.choice(categories)
            game = create_game(user, rand_category, icon=image_icon,
                               image=image_game)
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
