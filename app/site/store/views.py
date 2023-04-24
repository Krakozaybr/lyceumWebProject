from operator import or_

from flask import Blueprint, render_template, abort, redirect
from flask_login import current_user, login_required
from sqlalchemy import false, func

from app import settings
from app.models.chest import Chest
from app.models.comment import Comment
from app.models.db_session import create_session
from app.models.item import Item
from app.models.item_type import ItemType
from app.models.product import Product
from app.models.transaction import Transaction
from app.site.store.forms import (
    ProductCreateForm,
    ProductEditForm,
    ProductBuyForm,
    CommentForm,
)
from app.utils.models_utils import items_to_dict
from sqlalchemy.sql.expression import true

blueprint = Blueprint("store", __name__, template_folder=settings.TEMPLATES_DIR)


@blueprint.route("/")
def home():
    with create_session() as session:

        data = {
            "chests": session.query(Chest).all(),
            "products": session.query(Product).order_by(func.random()).limit(2).all(),
            "comments": session.query(Comment).order_by(Comment.date.desc()).limit(4).all(),
        }

        return render_template("store/home.html", **data)


@blueprint.route("/inventory")
@login_required
def inventory():
    items = items_to_dict([item for item in current_user.items if item.is_free])
    data = {"items": items}

    return render_template("store/inventory.html", **data)


@blueprint.route("/create_product/<int:item_type_id>", methods=["POST", "GET"])
@login_required
def create_product(item_type_id):
    with create_session() as session:

        item_type = session.query(ItemType).filter(ItemType.id == item_type_id).first()

        if item_type is None:
            abort(404)

        items = session.query(Item).filter(
            Item.user_id == current_user.id,
            Item.type_id == item_type_id,
            Item.is_free == true(),
        )

        if items.first() is None:
            abort(409)

        items_count = items.count()

        form = ProductCreateForm()
        if form.validate_on_submit():
            count = form.count.data
            if count > items_count or count <= 0:
                abort(409)

            product = Product()
            product.user_description = form.description.data
            product.user_id = current_user.id
            product.count = count
            product.item_type_id = item_type_id
            product.price = form.price.data

            for item in items.limit(count).all():
                item.is_free = False
                session.add(item)

            product.save_model(session)

            url = product.url

            return redirect(url)

        data = {"item_type": item_type, "max_count": items_count, "form": form}

        return render_template("store/product.html", **data)


@blueprint.route("/product/<int:pk>", methods=["POST", "GET"])
@login_required
def product_view(pk):
    with create_session() as session:
        product: Product = session.query(Product).filter(Product.id == pk).first()

        if product is None:
            abort(404)

        data = {
            "product": product,
            "comments": session.query(Comment)
            .filter(Comment.target_id == pk)
            .limit(4)
            .all(),
        }

        if current_user.id == product.user_id or current_user.is_staff:
            form = ProductEditForm()
            free_items = session.query(Item).filter(
                Item.user_id == product.user_id,
                Item.type_id == product.item_type_id,
                Item.is_free == true(),
            )

            data["form"] = form
            data["max_count"] = free_items.count() + product.count

            if form.validate_on_submit():

                product_items = session.query(Item).filter(
                    Item.user_id == product.user_id,
                    Item.type_id == product.item_type_id,
                    Item.is_free == false(),
                )

                count = form.count.data

                if count < product.count:
                    for item in product_items.limit(product.count - count).all():
                        item.is_free = True
                        session.add(item)
                elif count > product.count:
                    delta = count - product.count
                    if delta > free_items.count():
                        abort(409)
                    for item in free_items.limit(delta).all():
                        item.is_free = False
                        session.add(item)

                product.price = form.price.data
                product.user_description = form.description.data
                product.count = count

                session.commit()

                session.refresh(product)

            form.id.data = product.id
            form.price.data = product.price
            form.count.data = product.count
            form.description.data = product.user_description

            return render_template("store/product.html", **data)

        form = ProductBuyForm()
        comment_form = CommentForm()

        data["form"] = form
        data["comment_form"] = comment_form

        if form.validate_on_submit():
            count = form.count.data
            cost = count * product.price
            if cost > current_user.bill or count > product.count:
                abort(409)
            items = (
                session.query(Item)
                .filter(Item.user_id == product.user_id, Item.is_free == false())
                .limit(count)
                .all()
            )

            for item in items:
                item.is_free = True
                session.add(item)

            product.count -= count

            transaction = Transaction()
            transaction.from_user = product.user
            transaction.to_user = current_user
            transaction.items = items
            transaction.money = cost

            transaction.apply(session)

            if not product.count:
                session.delete(product)
                session.commit()

                return redirect("/products")

            session.commit()
            form.count.data = 0

        if comment_form.validate_on_submit():
            comment = Comment()
            comment.text = comment_form.text.data
            comment.target = product
            comment.user_id = current_user.id
            session.add(comment)
            session.commit()

            data["comments"] = (
                session.query(Comment).filter(Comment.target_id == pk).limit(4).all()
            )

            comment_form.text.data = ""

        return render_template("store/product_view.html", **data)


@blueprint.route("/transaction/<int:pk>")
@login_required
def transaction_view(pk):
    with create_session() as session:
        transaction: Transaction = (
            session.query(Transaction).filter(Transaction.id == pk).first()
        )

        if transaction is None:
            abort(404)

        data = {"transaction": transaction}

        if (
            current_user.id == transaction.from_user_id
            or current_user.id == transaction.to_user_id
            or current_user.is_staff
        ):
            return render_template("transactions/transaction.html", **data)

        abort(403)


@blueprint.route("/products")
@login_required
def products_view():
    with create_session() as session:
        data = {"products": session.query(Product).all()}

        return render_template("store/products.html", **data)


@blueprint.route("/transactions")
@login_required
def transactions_view():
    with create_session() as session:
        transactions = (
            session.query(Transaction)
            .filter(
                or_(
                    Transaction.to_user_id == current_user.id,
                    Transaction.from_user_id == current_user.id,
                )
            )
            .order_by(Transaction.created_at.desc())
        )
        data = {"transactions": transactions}

        return render_template("transactions/transactions.html", **data)


@blueprint.route("/comments/<int:product_id>")
@login_required
def comments_view(product_id):
    with create_session() as session:
        product: Product = session.query(Product).filter(Product.id == product_id).first()

        if product is None:
            abort(404)

        data = {"comments": product.comments, "product_id": product_id}

        return render_template("store/comments.html", **data)
