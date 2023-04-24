from flask import Blueprint, jsonify, request, abort
from flask_login import current_user

from app.models.item_type import ItemType
from app.models.db_session import create_session

blueprint = Blueprint("api_items", __name__)


@blueprint.route("/api/delete_item/<int:pk>", methods=["DELETE"])
def delete_item(pk):
    with create_session() as session:
        item_type = session.query(ItemType).filter(ItemType.id == pk).first()

        if item_type is None:
            abort(404)

        session.delete(item_type)
        session.commit()
    return jsonify({})
