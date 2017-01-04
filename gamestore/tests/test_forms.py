import pytest
from faker import Faker

from gamestore.forms import GameForm

fake = Faker()


@pytest.mark.skip
def test_game_form():
    # TODO: incomplete
    form = GameForm({
        'title': fake.text(30),
        'description': fake.text(),
        'category': fake.text(30),
        'price': fake.pydecimal(left_digits=2, right_digits=2, positive=True),
        'url': fake.url(),
        'icon': '',
        'image': '',
    },)
    assert form.is_valid()
