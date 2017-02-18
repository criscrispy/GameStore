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

import hypothesis.strategies as st
import pytest
from faker import Faker
from hypothesis import given
from hypothesis import settings

from gamestore.models import UserProfile
from gamestore.tests.create_content import create_game, \
    create_category, create_game_sale

settings.register_profile('dev', settings(max_examples=10))
# env = os.getenv(u'HYPOTHESIS_PROFILE', 'default')
# settings.load_profile(env)
settings.load_profile('dev')


fake = Faker()
GET = 'GET'
POST = 'POST'

STATUS_CODES = {
    'HttpResponsePermanentRedirect': 301,
    'HttpResponseRedirect': 302,
    'HttpResponseNotModified': 304,
    'HttpResponseBadRequest': 400,
    'HttpResponseNotFound': 404,
    'HttpResponseForbidden': 403,
    'HttpResponseNotAllowed': 405,
    'HttpResponseGone': 410,
    'HttpResponseServerError': 500,
}

# TODO: urlencode

# -----------------------------------------------------------------------------
# Strategies
# -----------------------------------------------------------------------------


def user_id_strategy():
    """Positive integer"""
    return st.integers(min_value=0, max_value=10000)


def game_id_strategy():
    """Positive integer"""
    return st.integers(min_value=0, max_value=10000)


# -----------------------------------------------------------------------------
# Base
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_index(client):
    """Test index page."""
    response = client.get('/')
    assert response.status_code == 200

    response = client.get('/?q=foobar')
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


@given(game_id=game_id_strategy())
@pytest.mark.django_db
def test_categories_detail(client, game_id):
    url = '/categories/{game_id}'
    response = client.get(url.format(game_id=game_id))
    assert response.status_code == 200


@pytest.mark.django_db
def test_publishers(client):
    url = '/publishers'
    response = client.get(url)
    assert response.status_code == 200


@given(game_id=game_id_strategy())
@pytest.mark.django_db
def test_publisher_detail(client, game_id):
    url = '/publishers/{user_id}'
    response = client.get(url.format(user_id=game_id))
    assert response.status_code == 200


# -----------------------------------------------------------------------------
# Accounts
# -----------------------------------------------------------------------------


def test_profile(client, admin_user):
    """Test profile."""
    url = '/accounts/profile'

    # Not logged in
    response = client.get(url)
    assert response.status_code == 302

    # Login
    client.login(username=admin_user.username, password='password')

    # Profile is configured as creation of user
    response = client.get(url)
    assert response.status_code == 200


def test_profile_edit(client, admin_user):
    """Test profile edit"""
    url = '/accounts/edit/profile'

    # Not logged in
    response = client.get(url)
    assert response.status_code == 302

    # Login
    client.login(username=admin_user.username, password='password')

    # GET
    response = client.get(url)
    assert response.status_code == 200

    # POST
    response = client.post(url, {})
    assert response.status_code == 302


# -----------------------------------------------------------------------------
# Players
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_game_detail(client, admin_user):
    category = create_category()
    game = create_game(admin_user, category)
    url = '/games/{game_id}/'

    # Requested game exists
    response = client.get(url.format(game_id=game.id))
    assert response.status_code == 200

    # Requested game does not exist
    response = client.get(url.format(game_id=game.id + 1))
    assert response.status_code == 404


@pytest.mark.django_db
def test_game_buy(client, admin_user):
    category = create_category()
    game = create_game(admin_user, category)
    url = '/games/{game_id}/buy'

    # Not logged in
    response = client.get(url.format(game_id=game.id))
    assert response.status_code == 302

    # Login
    client.login(username=admin_user.username, password='password')

    # Requested game exists
    response = client.get(url.format(game_id=game.id))
    assert response.status_code == 200

    # Requested game does not exist
    response = client.get(url.format(game_id=game.id + 1))
    assert response.status_code == 404


@pytest.mark.django_db
def test_game_play(client, admin_user):
    category = create_category()
    game = create_game(admin_user, category)

    url = '/games/{game_id}/play'

    # Not logged in
    response = client.get(url.format(game_id=game.id))
    assert response.status_code == 302

    # Login
    client.login(username=admin_user.username, password='password')

    # Game not bought
    response = client.get(url.format(game_id=game.id))
    assert response.status_code == 200

    # Create game sale
    create_game_sale(admin_user, game)

    # Game bought
    response = client.get(url.format(game_id=game.id))
    assert response.status_code == 200

    # Game does not exist
    response = client.get(url.format(game_id=game.id + 1))
    assert response.status_code == 404


@pytest.mark.django_db
def test_game_sale(client, admin_user):
    url = '/games/user/{user_id}'

    # Not logged in
    response = client.get(url.format(user_id=admin_user.id))
    assert response.status_code == 302

    # Login
    client.login(username=admin_user.username, password='password')

    # Logged in, profile does exists
    response = client.get(url.format(user_id=admin_user.id))
    assert response.status_code == 200

    # User id does not exist
    # FIXME: Raised errors in tests
    # response = client.get(url.format(user_id=admin_user.id + 1))
    # assert response.status_code == 404


@pytest.mark.skip
def test_game_like(client):
    assert True


# -----------------------------------------------------------------------------
# Developers
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_uploads(client, admin_user):
    category = create_category()
    game = create_game(admin_user, category)
    url = '/uploads/{user_id}'

    # One game published
    response = client.get(url.format(user_id=admin_user.id))
    assert response.status_code == 200

    # No games published / User does not exist
    response = client.get(url.format(user_id=admin_user.id + 1))
    assert response.status_code == 200


@pytest.mark.django_db
def test_upload(client, admin_user):
    url = '/upload'

    # Not logged in
    response = client.get(url)
    assert response.status_code == 302

    # Login
    client.login(username=admin_user.username, password='password')

    # Create profile
    # profile = create_profile(admin_user)
    profile = UserProfile.objects.get(user=admin_user)
    profile.developer_status = 1
    profile.save()

    # Profile found with developer status not allowing to upload
    response = client.get(url)
    assert response.status_code == 200

    # Developer status
    profile.developer_status = 2
    profile.save()

    # Profile found with developer status allowing to upload
    response = client.get(url)
    assert response.status_code == 200

    # TODO: test POST forms: valid | invalid


@pytest.mark.skip
def test_upload_detail():
    assert True


@pytest.mark.skip
def test_upload_stat():
    assert True


@pytest.mark.skip
def test_upload_edit():
    assert True


@pytest.mark.skip
def test_upload_delete():
    assert True
