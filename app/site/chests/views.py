from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required

from app import settings
from app.models.chest import Chest
from app.models.item_type import ItemType
from app.models.db_session import create_session
from app.site.authorization.decorators import staff_required

from .forms import ChestFormCreate, ChestFormEdit
from ...utils.utils import ImageFormatException, get_image, delete_img

blueprint = Blueprint("chests", __name__, template_folder=settings.TEMPLATES_DIR)


def fill_chest(chest: Chest, form, session):
    chest.name = form.name.data
    chest.description = form.description.data
    chest.items_count_min = form.items_count_min.data
    chest.items_count_max = form.items_count_max.data
    chest.coins_min = form.coins_min.data
    chest.coins_max = form.coins_max.data
    chest.price = form.price.data

    items = (
        session.query(ItemType)
        .filter(ItemType.id.in_(list(map(int, form.item_types.data.split(";")))))
        .all()
    )
    chest.item_types.clear()
    chest.item_types.extend(items)


@blueprint.route("/chest/create", methods=["POST", "GET"])
@login_required
@staff_required
def chest_create():
    form = ChestFormCreate()
    data = {"form": form}

    if form.validate_on_submit():

        try:
            filename = get_image(form.image.data)
        except ImageFormatException:
            return render_template(
                "chests/chest_crud.html",
                image_error="Расширение не поддерживается",
                **data
            )

        chest = Chest()

        with create_session() as session:
            fill_chest(chest, form, session)
            chest.image = filename
            chest.save_model(session)
            url = chest.url
            session.commit()

        return redirect(url)

    return render_template("chests/chest_crud.html", **data)


@blueprint.route("/chest/<int:pk>", methods=["POST", "GET"])
@login_required
@staff_required
def edit_chest(pk):
    with create_session() as session:
        chest = session.query(Chest).filter(Chest.id == pk).first()

        if chest is None:
            abort(404)

        form = ChestFormEdit()

        data = {"form": form, "image_url": chest.img_url}

        if form.validate_on_submit():

            filename = ""
            if form.image.data:
                try:
                    filename = get_image(form.image.data)
                except ImageFormatException:
                    return render_template(
                        "chests/chest_crud.html",
                        image_error="Расширение не поддерживается",
                        **data
                    )

            fill_chest(chest, form, session)

            if filename:
                delete_img(chest.image)
                chest.image = filename

            chest.save_model(session)
            url = chest.url
            session.commit()

            return redirect(url)

        form.id.data = chest.id
        form.name.data = chest.name
        form.description.data = chest.description
        form.items_count_min.data = chest.items_count_min
        form.items_count_max.data = chest.items_count_max
        form.coins_min.data = chest.coins_min
        form.coins_max.data = chest.coins_max
        form.price.data = chest.price
        form.item_types.data = ";".join(map(str, [i.id for i in chest.item_types]))

        return render_template("chests/chest_crud.html", **data)


@blueprint.route("/chests")
@staff_required
def chests():
    with create_session() as session:
        chests = session.query(Chest).all()

        return render_template("chests/chests.html", chests=chests)
