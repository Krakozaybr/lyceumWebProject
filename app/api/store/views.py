from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import false

from app.models.chest import Chest
from app.models.comment import Comment
from app.models.db_session import create_session
from app.models.item import Item
from app.models.product import Product

blueprint = Blueprint("api_store", __name__)


@blueprint.route("/api/buy", methods=["POST"])
@login_required
def buy():
    try:
        chest_id = int(request.json.get("chest_id", ""))
    except ValueError:
        return jsonify({"error": "No chest_id"}), 400

    with create_session() as session:
        chest: Chest = session.query(Chest).filter(Chest.id == chest_id).first()

        if chest is None:
            return jsonify({"error": "Chest doesn`t exist"}), 418  # I`,m teapot

        if chest.price > current_user.bill:
            return jsonify({"error": "Not enough money"})

        transaction = chest.open(current_user, session)

    return jsonify({"transaction": transaction.url})


@blueprint.route("/api/delete_product/<int:pk>", methods=["DELETE"])
@login_required
def remove_product(pk):
    with create_session() as session:
        product: Product = session.query(Product).filter(Product.id == pk).first()

        if product is None:
            return jsonify({"error": "Product doesn`t exist"}), 404

        if current_user.id != product.user_id and not current_user.is_staff:
            return jsonify({"error": "Not permitted"}), 403

        producted_items = (
            session.query(Item)
            .filter(Item.user_id == product.user_id, Item.is_free == false())
            .limit(product.count)
            .all()
        )
        for item in producted_items:
            item.is_free = True
            session.add(item)

        session.delete(product)
        session.commit()

    return jsonify({}), 200


@blueprint.route("/api/delete_comment/<int:pk>", methods=["DELETE"])
@login_required
def delete_comment(pk):
    with create_session() as session:
        comment: Comment = session.query(Comment).filter(Comment.id == pk).first()

        if comment is None:
            return jsonify({"error": "Comment doesn`t exist"}), 404

        if current_user.id != comment.user_id and not current_user.is_staff:
            return jsonify({"error": "Not permitted"}), 403

        session.delete(comment)
        session.commit()

    return jsonify({}), 200
