"""
http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
"""

from django.core.management.base import BaseCommand
from faker import Faker

from django.contrib.auth.models import User


# TODO: replace with django autofixture?
fake = Faker()


class Command(BaseCommand):
    """
    Populates the database with data for testing. Uses *faker* for data
    generation.
    """
    # args = '<arg1 arg2 ...>'
    help = 'Populates database with data for testing the website.'

    def _create_user(self):
        User.objects.create_user(fake.name(), fake.email(), password="test321")

    def create_admin(self):
        User.objects.create_superuser(fake.name(), fake.email(), password="test321")

    def handle(self, *args, **options):
        self._create_user()
