"""
https://buxty.com/b/2012/12/testing-django-haystack-whoosh/
"""
import pytest


@pytest.mark.skip
def test_search(client):
    """Test search"""
    url = '/search/{keyword}'
    response = client.get(url)
