from typing import Iterable


def get_extension(filename: str):
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename: str, allowed_extensions: Iterable[str]) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
