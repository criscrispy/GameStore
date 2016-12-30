import pytest


@pytest.mark.skip
def test_search(client):
    """Test search"""
    response = client.get('')
