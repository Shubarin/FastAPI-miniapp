import base64
import datetime
import imghdr
import os
from io import BytesIO

from fastapi import APIRouter, Form, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from PIL import Image as im
from pydantic.main import BaseModel
from sqlalchemy import desc

from data import db_session
from data.images import Image
from settings import DATABASES, STATIC_ROOT, VALID_EXTENSIONS
from utils.filename import get_filenames

router = APIRouter()


class Item(BaseModel):
    original: str
    negative: str
    pub_date: datetime.datetime


@router.get("/get_last_images", status_code=status.HTTP_200_OK)
async def get_last_images():
    db_sess = db_session.global_init(**DATABASES)
    last_images = db_sess.query(Image).order_by(desc(Image.pub_date)).limit(3).all()
    json_compatible_item_data = jsonable_encoder(last_images)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"last_images": json_compatible_item_data})


@router.post("/negative_image", status_code=status.HTTP_201_CREATED)
def negative_image(base64_image: str = Form(...)):
    decoded_string = base64.b64decode(base64_image)
    extension = imghdr.what(None, h=decoded_string)
    if extension not in VALID_EXTENSIONS:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            content={'error': 'bad file extensions'})
    original_fn, negative_fn = get_filenames(extension)
    original = im.open(BytesIO(decoded_string))
    inverted = im.eval(original, lambda x: 255 - x)
    original.save(os.path.join(STATIC_ROOT, original_fn))
    inverted.save(os.path.join(STATIC_ROOT, negative_fn))
    with open(os.path.join(STATIC_ROOT, negative_fn), 'rb') as image_read:
        image_64_encode = base64.b64encode(image_read.read())
    db_sess = db_session.global_init(**DATABASES)
    image = Image(original=original_fn, negative=negative_fn)
    db_sess.add(image)
    db_sess.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=str(image_64_encode))
