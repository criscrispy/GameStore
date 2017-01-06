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

GET = 'GET'
POST = 'POST'


def test_index(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200


def test_profile_not_logged(client):
    """Test profile when not logged in."""
    response = client.get('/accounts/profile')
    assert response.status_code == 302


def test_profile_logged(admin_client):
    """Test profile when loggen in."""
    response = admin_client.get('/accounts/profile')
    assert response.status_code == 200


@pytest.mark.django_db
def test_games(client):
    response = client.get('/games')
    assert response.status_code == 200


def test_game_detail():
    assert True


def test_game_play():
    assert True


def test_game_buy():
    assert True


def test_categories():
    assert True


def test_categories_detail():
    assert True


def test_game_sale():
    assert True


def test_uploads():
    assert True


def test_publishers():
    assert True


def test_publisher_detail():
    assert True


def test_apply_developer():
    assert True
