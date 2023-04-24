from flask import Blueprint

from app import settings
from app.api.utils.views import blueprint as utils
from app.api.store.views import blueprint as store
from app.api.items.views import blueprint as items
from app.api.chests.views import blueprint as chests

api = Blueprint("api", __name__, template_folder=settings.TEMPLATES_DIR)

api.register_blueprint(utils)
api.register_blueprint(store)
api.register_blueprint(items)
api.register_blueprint(chests)
