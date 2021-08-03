import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

DATABASES = {
    'ENGINE': os.environ.get('DB_ENGINE', 'postgresql+psycopg2'),
    'USER': os.environ.get('DB_USER', 'postgres'),
    'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
    'HOST': os.environ.get('DB_HOST', 'localhost'),
    'PORT': os.environ.get('DB_PORT', 5432),
    'NAME': os.environ.get('DB_NAME', 'FastAPI'),
}

API_PREFIX = '/api/v1'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

VALID_EXTENSIONS = {
    'jpg',
    'jpeg',
    'png'
}