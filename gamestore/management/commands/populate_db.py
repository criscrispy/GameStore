"""
http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
"""
import os
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from gamestore.models import Game
from django.core.files import File


# TODO: replace with django autofixture?
fake = Faker()


def create_user(superuser=False):
    """

    Args:
        superuser (boolean): Create superuser

    Returns:
        User: Created user
    """
    d = dict(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password="password321"
    )

    if not superuser:
        return User.objects.create_user(**d)
    else:
        return User.objects.create_superuser(**d)


def create_image(name, width=50, height=50):
    """
    Test image creation adapted from

    http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/

    Args:
        name (str):
        width (int):
        height (int):

    Returns:
        BytesIO: Test image
    """
    ext = "png"
    file = BytesIO()
    image = Image.new('RGBA', size=(width, height), color=(155, 0, 0))
    image.save(file, format=ext)
    file.name = name + '.' + ext
    file.seek(0)
    return file


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


class Command(BaseCommand):
    """
    Populates the database with data for testing. Uses *faker* for data
    generation.
    """
    args = '<amount>'
    help = 'Populates database with data for testing the website.'

    def handle(self, *args, **options):
        # TODO: Add amount
        user = create_user()
        image_path = create_image("test")
        game = create_game(user, image=image_path)
