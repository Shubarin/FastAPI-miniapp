import base64

from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc

from api.api import api_router
from api.endpoints.images import negative_image as api_negative_images
from data import db_session
from data.images import Image
from settings import API_PREFIX, DATABASES, TEMPLATES_DIR

app = FastAPI()

app.include_router(api_router, prefix=API_PREFIX)
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/get_last_images/")
@app.get("/")
async def get_last_images(request: Request) -> templates.TemplateResponse:
    """
    Returns an html template with the last three uploaded images
    :param request:
    :return templates.TemplateResponse:
    """
    db = db_session.global_init(**DATABASES)
    last_images = db.query(Image).order_by(desc(Image.pub_date)).limit(3).all()
    return templates.TemplateResponse("index.html",
                                      context={
                                          "request": request,
                                          "last_images": last_images
                                      })


@app.post("/negative_image/")
async def negative_image(upload_file: bytes = File(...)) -> JSONResponse:
    """
    Returns the result of converting an image to a negative
    :param upload_file:
    :return JSONResponse:
    """
    return api_negative_images(base64.b64encode(upload_file).decode('ascii'))


@app.get("/negative_image/", response_class=HTMLResponse)
async def negative_image(request: Request) -> templates.TemplateResponse:
    """
    Page for uploading an image
    :param request:
    :return templates.TemplateResponse:
    """
    return templates.TemplateResponse("upload_file.html",
                                      context={"request": request})
