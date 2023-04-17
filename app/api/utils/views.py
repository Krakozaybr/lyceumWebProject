from flask import Blueprint, jsonify, request

from app.models.users.user_registrator import LoginValidator

blueprint = Blueprint("api_utils", __name__)


@blueprint.route("/api/login_available", methods=["POST"])
def login_valid():
    login = request.json.get("login", None)

    validator = LoginValidator(login)

    return jsonify({"is_available": validator.validate(), "error": validator.error()})
