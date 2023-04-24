from flask import Blueprint, jsonify, request, abort
from flask_login import current_user

from app.models.chest import Chest
from app.models.db_session import create_session

blueprint = Blueprint("api_chests", __name__)


@blueprint.route("/api/delete_chest/<int:pk>", methods=["DELETE"])
def delete_chest(pk):
    with create_session() as session:
        item_type = session.query(Chest).filter(Chest.id == pk).first()

        if item_type is None:
            abort(404)

        session.delete(item_type)
        session.commit()

    return jsonify({})
