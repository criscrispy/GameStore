"""
Test content creation.
"""
import string

import hypothesis.strategies as st
from hypothesis import given

from gamestore.tests.create_content import BITMAP, SVG, create_image


@given(
    name=st.text(alphabet=string.ascii_letters, min_size=1, max_size=8),
    width=st.integers(min_value=1, max_value=1000),
    height=st.integers(min_value=1, max_value=1000),
    choice=st.choices(),
    text=st.text(alphabet=string.ascii_letters, min_size=1, max_size=8)
)
def test_create_image(name, width, height, choice, text):
    filetype = choice(BITMAP)
    image = create_image(name, width, height, filetype, text)
    assert True
