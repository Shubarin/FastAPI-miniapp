import base64
from io import BytesIO

from PIL import Image


def img_to_base64_str(image: Image, extension: str) -> str:
    """
    Saves the image in a temporary buffer, returns its string representation
    :param image:
    :param extension:
    :return str:
    """
    buffered_original = BytesIO()
    image.save(buffered_original, format=extension)
    return base64.b64encode(buffered_original.getvalue()).decode('ascii')
