import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from gamestore.tests.create_content import create_image, create_user, \
    create_profile, create_game, create_score, create_game_sale, create_category


def populate(user_amount, game_amount, sales_amount, scores_amount):
    image_game = create_image("image", width=128, height=128)
    image_icon = create_image("icon", width=48, height=48)
    image_profile = create_image("profile", width=128, height=128)

    users = []
    categories = []
    games = []
    sales = []
    sales_dict = {}
    category_titles = [
        '3D', 'Action', 'Adventure', 'Alien', 'Arcade',
        'Card', 'Dress Up', 'Fantasy', 'Fighting', 'Flying',
        'Football',
        'Golf', 'Holidays', 'Kids', 'Multiplayer', 'Pool',
        'Puzzle',
        'Racing', 'Simulation', 'Sports', 'Strategy',
        'Winter', 'Word', 'Zombie'
    ]

    for i in range(user_amount):
        try:
            user = create_user()
        except IntegrityError:
            # Tries to create new user with existing username
            continue
        create_profile(user, image=image_profile)
        users.append(user)

    if users:
        for title in category_titles:
            category = create_category(title)
            categories.append(category)

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
    # TODO: Add arguments
    args = '<amount>'
    help = 'Populates database with data for testing the website.'

    def handle(self, *args, **options):
        populate(10, 50, 10, 10)
