import base64
import json

from fastapi import FastAPI, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc

from api.api import api_router
from api.endpoints.images import negative_image as api_negative_images
from data import db_session
from data.images import Image
from settings import API_PREFIX, DATABASES


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router, prefix=API_PREFIX)
templates = Jinja2Templates(directory="templates")


@app.get("/get_last_images/")
@app.get("/")
async def get_last_images(request: Request) -> json:
    db_sess = db_session.global_init(**DATABASES)
    last_images = db_sess.query(Image).order_by(desc(Image.pub_date)).limit(3).all()
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "last_images": last_images})


@app.post("/negative_image/")
async def negative_image(upload_file: bytes = File(...)):
    return api_negative_images(base64.b64encode(upload_file).decode('ascii'))


@app.get("/negative_image/", response_class=HTMLResponse)
async def negative_image(request: Request):
    return templates.TemplateResponse("upload_file.html", {"request": request})
