from flask import Flask

from app.models import db_session
from app.models.core import format_date
from app.settings import DB_FILE, STATIC_DIR
from app.site.authorization.views import login_manager
from app.api.api import api
from app.site.views import blueprint as site

app = Flask(__name__, static_folder=STATIC_DIR)
app.config["SECRET_KEY"] = "yandexlyceum1_secret_key"

login_manager.init_app(app)

app.register_blueprint(api)
app.register_blueprint(site)


@app.template_filter()
def date(value):
    return format_date(value)


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db.session.remove()


def main():
    db_session.global_init(DB_FILE)
    app.run()


if __name__ == "__main__":
    main()
