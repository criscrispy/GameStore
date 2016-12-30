"""
Test content creation.
"""
import os
import shutil
import string
from io import BytesIO, StringIO

import hypothesis.strategies as st
from hypothesis import given, settings

from gamestore.tests.create_content import BITMAP, SVG, create_image


# TODO: BASE_DIR
SAVE_IMAGES = False
IMAGES_FOLDER = ".test_images"

# Directory for saving images
if SAVE_IMAGES:
    if os.path.exists(IMAGES_FOLDER):
        shutil.rmtree(IMAGES_FOLDER)
    os.makedirs(IMAGES_FOLDER)


def save_image(image):
    """

    Args:
        image (BytesIO|StringIO):
    """
    if isinstance(image, BytesIO):
        mode = 'wb'
    elif isinstance(image, StringIO):
        mode = 'wt'
    else:
        raise Exception()
    with open(os.path.join(IMAGES_FOLDER, image.name), mode) as file:
        shutil.copyfileobj(image, file)


@settings(max_examples=10)
@given(
    name=st.text(alphabet=string.ascii_letters, min_size=1, max_size=8),
    width=st.integers(min_value=1, max_value=1000),
    height=st.integers(min_value=1, max_value=1000),
    choice=st.choices(),
    text=st.text(alphabet=string.ascii_letters, min_size=1, max_size=8) or
         st.none()
)
def test_create_image(name, width, height, choice, text):
    # TODO: image size choices
    filetype = choice(BITMAP + SVG)
    image = create_image(name, width, height, filetype, text)
    assert isinstance(image, (BytesIO, StringIO))

    # Save images to file
    if SAVE_IMAGES:
        save_image(image)
