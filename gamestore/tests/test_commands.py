import pytest

from gamestore.management.commands.populate_db import populate


@pytest.mark.django_db
def test_populate():
    populate(user_amount=1, game_amount=1, sales_amount=1, scores_amount=1)
    assert True
