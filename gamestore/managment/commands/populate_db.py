"""
http://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database
"""

from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    """
    Populates the database with data for testing. Uses *faker* for data
    generation.
    """
    def handle(self, *args, **options):
        pass
