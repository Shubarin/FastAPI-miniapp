import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

API_PREFIX = "/api/v1"

VALID_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}
