from flask import Flask

from app.models import db_session
from app.settings import DB_FILE, STATIC_DIR
from app.site.authorization.views import blueprint as auth, login_manager
from app.api.utils.views import blueprint as utils_api

app = Flask(
    __name__, static_folder=STATIC_DIR
)
app.config["SECRET_KEY"] = "yandexlyceum1_secret_key"
app.register_blueprint(auth)
app.register_blueprint(utils_api)
login_manager.init_app(app)


def main():
    db_session.global_init(DB_FILE)
    app.run()


if __name__ == "__main__":
    main()
