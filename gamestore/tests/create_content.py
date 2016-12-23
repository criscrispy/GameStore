from io import BytesIO

from PIL import Image

BITMAP = ('jpeg', 'png', 'gif', 'ico')
SVG = ('svg',)


def create_image(name, width=50, height=50, filetype='png', text=None):
    """
    Creates in memory images for testing.

    Args:
        name (str): Name without file extension.
        width (int): Positive integer
        height (int): Positive integer
        filetype (str): Bitmap {'jpg', 'jpeg', 'png', 'gif', 'ico'}
                        Vector graphics {'svg'}
        text (str, optional): None uses default "{width}x{height}" string.
                    Otherwise supplied string is used if string is empty
                    no text is set.

    Returns:
        BytesIO: Image as BytesIO object. It can be used in same fashion as
            file object
            >>> file = open("image.ext", 'rb')
            created by opening a file.

    Todo:
        Formats: jpg, png, gif, svg, ico
        Text in the figure
        Width and height units

    Resources:

    .. [#] http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
    .. [#] https://svgwrite.readthedocs.io/en/latest/overview.html
    """
    # TODO: text into image
    if text is None:
        text = "{width}x{height}".format(width=width, height=height)

    file = BytesIO()
    file.name = name + '.' + filetype

    if filetype in BITMAP:
        image = Image.new('RGBA', size=(width, height), color=(128, 128, 128))
        # TODO: Text
        image.save(file, format=filetype)
    elif filetype in SVG:
        # FIXME: Change BytesIO -> StringIO
        import svgwrite
        center = (width / 2, height / 2)
        image = svgwrite.Drawing(file.name, profile='tiny',
                                 height=height, width=width)
        image.add(image.rect(center, (width, height)))
        image.add(image.text(text, center))
        # image.write(file)
        raise NotImplementedError
    else:
        raise Exception('Filetype "{}" not in "{}"'.format(
            filetype, BITMAP.union(SVG)))

    file.seek(0)
    return file