from flask import Blueprint

from app import settings
from .authorization.views import blueprint as auth
from .items.views import blueprint as items
from .store.views import blueprint as store
from .chests.views import blueprint as chests

blueprint = Blueprint("site", __name__, template_folder=settings.TEMPLATES_DIR)
blueprint.register_blueprint(auth)
blueprint.register_blueprint(items)
blueprint.register_blueprint(store)
blueprint.register_blueprint(chests)
