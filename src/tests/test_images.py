import base64
import os
import shutil
from io import BytesIO

import numpy as np
from PIL import Image

from ..app.settings import API_PREFIX


def test_api_get_latest_images_check_number_result_low_or_equals_3(test_app):
    """
    Testing the number of returned results
    :param test_app:
    :return:
    """
    resource = f"{API_PREFIX}/get_last_images"
    latest_images = test_app.get(resource).json().get("last_images", None)
    assert latest_images is not None, ("Bad type of response, a list was "
                                       "expected, but None came")

    assert len(latest_images) <= 3, (f"Expected len(latest_image) <= 3, "
                                     f"but {len(latest_images)} came")


def test_api_get_latest_images_check_sort_result_to_date(test_app):
    """
    Testing sorting returned latest images
    :param test_app:
    :return:
    """
    resource = f"{API_PREFIX}/get_last_images"
    latest_images = test_app.get(resource).json().get("last_images", None)
    if len(latest_images) > 1:
        assert latest_images[0]["pub_date"] >= latest_images[-1]["pub_date"]

    if len(latest_images) > 2:
        assert (latest_images[0]["pub_date"] >=
                latest_images[1]["pub_date"] >=
                latest_images[2]["pub_date"])


def test_api_post_negative_image_check_incorrect_extensions(test_app):
    """
    Checking that the wrong data type will not be processed
    :param test_app:
    :return:
    """
    resource = f"{API_PREFIX}/negative_image"
    os.mkdir("tmp")
    filenames = ("tmp/file.txt", "tmp/file", "tmp/file.pdf",
                 "tmp/file.docx", "tmp/file.py")
    for filename in filenames:
        open(filename, "wb")
        data = {"base64_image": base64.b64encode(
            open(filename, 'rb').read()).decode('ascii')}
        response = test_app.post(resource, data=data)
        assert response.status_code == 422, (f"Bad extension, status code "
                                             f"{response.status_code} != 422")
    incorrect_strings = ("b'x8/sadk/l2jk91;a'", "asdfg", "12345", "")
    for line in incorrect_strings:
        response = test_app.post(resource, data=line)
        assert response.status_code == 422, (f"Bad extension, status code "
                                             f"{response.status_code} != 422")
    shutil.rmtree("tmp")


def test_api_post_negative_image_check_correct_extensions(test_app):
    """
    Checking that the correct data type will be processed
    :param test_app:
    :return:
    """
    resource = f"{API_PREFIX}/negative_image"
    os.mkdir("tmp")
    filenames = ("tmp/file.jpg", "tmp/file.jpeg", "tmp/file.png")
    pixels = [[(255, 255, 255)]]
    array = np.array(pixels, dtype=np.uint8)
    new_image = Image.fromarray(array)
    for filename in filenames:
        new_image.save(filename)
        data = {"base64_image": base64.b64encode(
            open(filename, "rb").read()).decode("ascii")}
        response = test_app.post(resource, data=data)
        assert response.status_code == 201, (f"Bad extension, status code "
                                             f"{response.status_code} != 201")
    shutil.rmtree("tmp")


def test_api_post_negative_image_check_empty_file(test_app):
    """
    Checking that the empty data type will not be processed
    :param test_app:
    :return:
    """
    resource = f"{API_PREFIX}/negative_image"
    response = test_app.post(resource)
    assert response.status_code == 422, (f"Bad extension, status code "
                                         f"{response.status_code} != 422")


def test_api_negative_image_check_result_image_color(test_app):
    """
    Checking the correctness of converting colors to negative
    :param test_app:
    :return:
    """
    resource = f"{API_PREFIX}/negative_image"
    # random color of points
    pixel_cases = [
        [[(255, 255, 255)]],
        [[(139, 215, 57)]],
        [[(0, 0, 0)]]
    ]
    for pixels in pixel_cases:
        array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save("test.jpg")
        data = {"base64_image": base64.b64encode(
            open("test.jpg", "rb").read()).decode("ascii")}
        response = test_app.post(resource, data=data)
        decoded_string = base64.b64decode(response.json().get("negative"))
        im = Image.open(BytesIO(decoded_string))
        new_pixels = np.asarray(im)[0][0]
        assert (255 - pixels[0][0][0]) == new_pixels[0], "Bad inverted Red"
        assert (255 - pixels[0][0][1]) == new_pixels[1], "Bad inverted Green"
        assert (255 - pixels[0][0][2]) == new_pixels[2], "Bad inverted Blue"
