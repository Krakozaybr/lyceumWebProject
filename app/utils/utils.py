import os
import uuid
from typing import Iterable

from flask import url_for

from app import settings


def get_extension(filename: str):
    return filename.rsplit(".", 1)[1].lower()


def allowed_file(filename: str, allowed_extensions: Iterable[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


class ImageFormatException(Exception):
    pass


def get_image(data):
    if not allowed_file(data.filename, settings.ALLOWED_IMAGES_EXTENSIONS):
        raise ImageFormatException

    filename = str(uuid.uuid4())
    while os.path.exists(filename):
        filename = str(uuid.uuid4())

    filename += "." + get_extension(data.filename)
    data.save(os.path.join(settings.IMAGES_DIR, filename))

    return filename


def delete_img(filename: str):
    way = os.path.join(settings.IMAGES_DIR, filename)
    if os.path.exists(way):
        os.remove(way)


def img_url(img_name: str):
    return url_for("static", filename=f"{settings.IMAGES_DIR_NAME}/{img_name}")
