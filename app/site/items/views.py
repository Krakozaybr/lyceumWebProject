from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required

from app import settings
from app.models.item_type import ItemType
from app.site.authorization.decorators import staff_required
from .forms import ItemTypeFormCreate, ItemTypeFormEdit
from ...models.db_session import create_session
from ...utils.utils import get_image, ImageFormatException, delete_img

blueprint = Blueprint("items", __name__, template_folder=settings.TEMPLATES_DIR)


@blueprint.route("/item_type/create", methods=["POST", "GET"])
@login_required
@staff_required
def add_item_type():
    form = ItemTypeFormCreate()
    data = {"form": form}

    if form.validate_on_submit():

        try:
            filename = get_image(form.image.data)
        except ImageFormatException:
            return render_template(
                "items/item_type_crud.html",
                image_error="Расширение не поддерживается",
                **data
            )

        item_type = ItemType()
        item_type.name = form.name.data
        item_type.description = form.description.data
        item_type.rare = form.rare.data

        item_type.image = filename

        with create_session() as session:
            item_type.save_model(session)
            url = item_type.url

        return redirect(url)

    return render_template("items/item_type_crud.html", **data)


@blueprint.route("/item_type/<int:pk>", methods=["POST", "GET"])
@login_required
@staff_required
def change_item_type(pk):
    with create_session() as session:
        item_type = session.query(ItemType).filter(ItemType.id == pk).first()

        if item_type is None:
            abort(404)

        form = ItemTypeFormEdit()

        form.id.data = item_type.id
        form.name.data = item_type.name
        form.description.data = item_type.description
        form.rare.data = item_type.rare

        data = {"form": form, "image_url": item_type.img_url}

        if form.validate_on_submit():

            filename = ""
            if form.image.data:
                try:
                    filename = get_image(form.image.data)
                except ImageFormatException:
                    return render_template(
                        "items/item_type_crud.html",
                        image_error="Расширение не поддерживается",
                        **data
                    )

            item_type.name = form.name.data
            item_type.description = form.description.data
            item_type.rare = form.rare.data

            if filename:
                delete_img(item_type.image)
                item_type.image = filename

            item_type.save_model(session)

            return redirect("/item_types")

        return render_template("items/item_type_crud.html", **data)


@blueprint.route("/item_types")
@login_required
def item_types_list():
    with create_session() as session:
        item_types = session.query(ItemType).all()

        return render_template("items/item_types.html", item_types=item_types)
