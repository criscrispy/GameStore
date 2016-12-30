"""
Pytest-django fixtures:
https://github.com/pytest-dev/pytest-django/blob/master/pytest_django/fixtures.py
"""
import pytest

# TODO: status codes
# TODO: Get | Post


def test_index(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200


def test_profile(client, admin_user):
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
