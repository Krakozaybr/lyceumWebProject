import os

BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_NAME = "db.sqlite"
DB_DIR = os.path.join(BASE_DIR, "db")
DB_FILE = os.path.join(DB_DIR, DB_NAME)
IMAGES_DIR_NAME = "images"
IMAGES_DIR = os.path.join(STATIC_DIR, IMAGES_DIR_NAME)
ALLOWED_IMAGES_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
