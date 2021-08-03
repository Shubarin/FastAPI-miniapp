import datetime as dt
import os
from typing import Tuple

from settings import STATIC_ROOT


def get_filenames(extension: str) -> Tuple[str, str]:
    date_now = dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    os.mkdir(STATIC_ROOT + f'/images/{date_now}')
    original_fn = f'images/{date_now}/original.{extension}'
    negative_fn = f'images/{date_now}/negative.{extension}'
    return original_fn, negative_fn
