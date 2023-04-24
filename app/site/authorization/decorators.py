from flask_login import current_user
from flask import abort
from functools import wraps


def staff_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_staff:
            abort(403)
        return func(*args, **kwargs)

    return decorated
