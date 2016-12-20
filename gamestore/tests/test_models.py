import pytest
from hypothesis.extra.django.models import models
from hypothesis import given
import hypothesis.strategies as st
from django.contrib.auth.models import User
from gamestore.models import Game, Score, GameSale
import string

from io import BytesIO
from PIL import Image


# Allow pytest database access
pytestmark = pytest.mark.django_db

# Hypothesis
# perform_health_check = False


# ----------
# Strategies
# ----------

def create_test_image():
    """
    Test image creation adapted from

    http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/

    Returns:
        BytesIO: Test image
    """
    file = BytesIO()
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


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
    icon=st.just("gamestore/tests/images/profile_48_48.png"),
    image=st.just("gamestore/tests/images/image_350_200.png"),
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
