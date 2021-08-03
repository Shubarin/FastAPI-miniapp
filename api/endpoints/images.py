import base64
import imghdr
from io import BytesIO

from fastapi import APIRouter, Form, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from PIL import Image as im
from sqlalchemy import desc

from data import db_session
from data.images import Image
from settings import DATABASES, VALID_EXTENSIONS
from utils.converter_img_to_base64_str import img_to_base64_str

router = APIRouter()


@router.get("/get_last_images", status_code=status.HTTP_200_OK)
async def get_last_images() -> JSONResponse:
    """
    Returns a list with the last three uploaded images
    :return JSONResponse:
    """
    db = db_session.global_init(**DATABASES)
    last_images = db.query(Image).order_by(desc(Image.pub_date)).limit(3).all()
    json_compatible_item_data = jsonable_encoder(last_images)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"last_images": json_compatible_item_data})


@router.post("/negative_image", status_code=status.HTTP_201_CREATED)
def negative_image(base64_image: str = Form(...)) -> JSONResponse:
    """
    Checks the type of the received image (JPEG, PNG are available -
    the full list can be configured in settings.VALID_EXTENSIONS set).
    In the case of a correct file, it performs a conversion to a negative
    and saves both images to the database row with the following fields:
    image.original - str base64
    image.negative - str base64
    image.type - str

    :param base64_image:
    :return JSONResponse:
    """
    decoded_string = base64.b64decode(base64_image)
    extension = imghdr.what(None, h=decoded_string)
    if extension not in VALID_EXTENSIONS:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content={'error': 'bad file extensions'})
    original = im.open(BytesIO(decoded_string))
    inverted = im.eval(original, lambda x: 255 - x)
    db_sess = db_session.global_init(**DATABASES)
    original = img_to_base64_str(original, extension)
    inverted = img_to_base64_str(inverted, extension)
    image = Image(original=original, negative=inverted, type=extension)
    db_sess.add(image)
    db_sess.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"id": image.id,
                                 "type": image.type,
                                 "original": image.original,
                                 "negative": image.negative})
