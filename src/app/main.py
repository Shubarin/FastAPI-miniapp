import base64

from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .api.api import api_router
from .api.endpoints.images import negative_image as api_negative_images
from .db import database, engine, metadata
from .settings import API_PREFIX, TEMPLATES_DIR

app = FastAPI()

metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


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
    conn = engine.connect()
    last_images = conn.execute(
        'SELECT * FROM images '
        'ORDER BY pub_date DESC '
        'LIMIT 3;'
    ).fetchall()
    return templates.TemplateResponse("index.html",
                                      context={
                                          "request": request,
                                          "last_images": last_images
                                      })


@app.post("/negative_image/")
async def negative_image(upload_file: bytes = File(...)) -> JSONResponse:
    """
    Received image (JPEG, PNG are available -
    the full list can be configured in settings.VALID_EXTENSIONS set).
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
