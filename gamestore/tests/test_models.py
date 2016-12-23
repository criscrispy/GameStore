import string

import pytest
import hypothesis.strategies as st
from django.contrib.auth.models import User
from hypothesis import given
from hypothesis.extra.django.models import models

from gamestore.models import Game, Score

# Allow pytest database access
pytestmark = pytest.mark.django_db

# Hypothesis
# perform_health_check = False


# ----------
# Strategies
# ----------


username_alphabet = string.ascii_letters + string.digits + "@.+-_"
password_alphabet = string.ascii_letters + string.digits + string.punctuation

user = models(
    User,
    username=st.text(username_alphabet, min_size=1, max_size=150),
    password=st.text(password_alphabet, min_size=8, max_size=128),
)

game = models(
    Game,
    publisher=user,
    title=st.text(max_size=30),
    description=st.text(max_size=1000),
    category=st.text(max_size=30),
    price=st.floats(min_value=0.0, allow_nan=False, allow_infinity=False),
    url=st.just("https://en.wikipedia.org/wiki/Uniform_Resource_Locator"),
    # TODO: In memory creation of images
    # icon=st.just("gamestore/tests/images/profile_48_48.png"),
    # image=st.just("gamestore/tests/images/image_350_200.png"),
)

score = models(
    Score,
    game=game,
    player=user,
    score=st.integers(0)
)


@given(model=user)
def test_user(model):
    assert True


@given(model=game)
def test_game(model):
    assert True


def test_score():
    assert True


def test_game_sale():
    assert True
