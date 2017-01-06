"""
Pytest-django fixtures:
https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py

HttpResponse

- Status codes

    - 1xx (Informational): The request was received, continuing process

    - 2xx (Successful): The request was successfully received,
      understood, and accepted

    - 3xx (Redirection): Further action needs to be taken in order to
      complete the request

    - 4xx (Client Error): The request contains bad syntax or cannot be
      fulfilled

    - 5xx (Server Error): The server failed to fulfill an apparently
      valid request

    https://tools.ietf.org/html/rfc7231.html#section-6

-  Methods

    - Get
    - Post
"""
import pytest
from faker import Faker

fake = Faker()
GET = 'GET'
POST = 'POST'

# TODO: urlencode


# -----------------------------------------------------------------------------
# Base
# -----------------------------------------------------------------------------


def test_index(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_games(client):
    """Test games page."""
    response = client.get('/games')
    assert response.status_code == 200


@pytest.mark.django_db
def test_categories(client):
    url = '/categories'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_categories_detail(client):
    game_id = fake.random_int(min=0)
    url = '/categories/{game_id}'.format(game_id=game_id)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_publishers(client):
    url = '/publishers'
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_publisher_detail(client):
    user_id = fake.random_int(min=0)
    url = '/publishers/{user_id}'.format(user_id=user_id)
    response = client.get(url)
    assert response.status_code == 200


# -----------------------------------------------------------------------------
# Accounts
# -----------------------------------------------------------------------------


def test_profile_not_logged(client):
    """Test profile when not logged in."""
    response = client.get('/accounts/profile')
    assert response.status_code == 302


def test_profile_logged(admin_client):
    """Test profile when loggen in."""
    response = admin_client.get('/accounts/profile')
    assert response.status_code == 200


# -----------------------------------------------------------------------------
# Players
# -----------------------------------------------------------------------------


def test_game_detail():
    assert True


def test_game_play():
    assert True


def test_game_buy():
    assert True


def test_game_sale():
    assert True


def test_game_like():
    assert True


# -----------------------------------------------------------------------------
# Developers
# -----------------------------------------------------------------------------


def test_uploads():
    assert True


def test_upload():
    assert True


def test_upload_detail():
    assert True


def test_upload_stat():
    assert True


def test_upload_edit():
    assert True


def test_upload_delete():
    assert True
