import pytest
from imagefactory import create_image

from gamestore.models import UserProfile
from gamestore.tests.create_content import create_user, \
    create_game, create_score, create_game_sale, create_category


@pytest.mark.django_db
def test_user():
    user = create_user()
    # New user profile should be created at the same time as new user
    # is created
    profile = UserProfile.objects.get(user=user)
    assert True


@pytest.mark.django_db
def test_game():
    user = create_user()
    category = create_category()
    image = create_image("image", width=128, height=128)
    icon = create_image("icon", width=48, height=48)
    game = create_game(user, category, icon=icon, image=image)
    assert True


@pytest.mark.django_db
def test_score():
    user = create_user()
    category = create_category()
    image = create_image("image", width=128, height=128)
    icon = create_image("icon", width=48, height=48)
    game = create_game(user, category, icon=icon, image=image)
    score = create_score(user, game)
    assert True


@pytest.mark.django_db
def test_game_sale():
    user = create_user()
    category = create_category()
    image = create_image("image", width=128, height=128)
    icon = create_image("icon", width=48, height=48)
    game = create_game(user, category, icon=icon, image=image)
    create_game_sale(user, game)
    assert True
