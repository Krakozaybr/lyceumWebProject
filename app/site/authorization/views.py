import os

from flask import Blueprint, redirect, render_template, request
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from .forms import (
    RegistrationForm,
    LoginForm,
    AvatarForm,
    ChangeDescriptionForm,
    ChangePasswordForm,
)

from app import settings
from ...models.db_session import create_session
from app.models.users.user import User
from ...models.users.user_registrator import UserRegistrator, PasswordValidator
import uuid

from ...utils.utils import allowed_file, get_extension

blueprint = Blueprint("authorization", __name__, template_folder=settings.TEMPLATES_DIR)
login_manager = LoginManager()
current_user: User


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session = create_session()

        user = session.query(User).filter(User.login == form.login.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "users/login.html",
            message="Неверный логин или пароль",
            title="Авторизация",
            form=form,
        )
    return render_template("users/login.html", title="Авторизация", form=form)


@blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        registrator = UserRegistrator(form.login.data, form.password.data)
        user_id = registrator.register()
        if user_id is not None:
            user = create_session().query(User).get(user_id)
            login_user(user, remember=True)
            return redirect("/")
        return render_template(
            "users/register.html", err=registrator.error(), form=form
        )
    return render_template("users/register.html", form=form)


@blueprint.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    avatar_form = AvatarForm()
    change_description_form = ChangeDescriptionForm()
    change_password_form = ChangePasswordForm()

    data = {
        "avatar_form": avatar_form,
        "change_description_form": change_description_form,
        "change_password_form": change_password_form,
        "description": current_user.description,
    }

    data_changed = False

    if avatar_form.validate_on_submit():

        data_changed = True

        if not allowed_file(
            avatar_form.image.data.filename, settings.ALLOWED_IMAGES_EXTENSIONS
        ):
            return render_template(
                "users/profile.html", image_error="Расширение не поддерживается", **data
            )

        filename = str(uuid.uuid4())
        while os.path.exists(filename):
            filename = str(uuid.uuid4())

        filename += '.' + get_extension(avatar_form.image.data.filename)

        if current_user.avatar:
            os.remove(os.path.join(settings.IMAGES_DIR, current_user.avatar))

        current_user.avatar = filename
        avatar_form.image.data.save(os.path.join(settings.IMAGES_DIR, filename))

    if change_password_form.validate_on_submit():

        data_changed = True

        if not current_user.check_password(change_password_form.password.data):
            return render_template(
                "users/profile.html",
                password_error="Указан неверный текущий пароль",
                **data
            )

        password_validator = PasswordValidator(
            password=change_password_form.new_password.data
        )

        if not password_validator.validate():
            return render_template(
                "users/profile.html", password_error=password_validator.error(), **data
            )

        current_user.set_password(change_password_form.new_password.data)

    if change_description_form.validate_on_submit():
        data_changed = True
        current_user.description = change_description_form.description.data

    if data_changed:
        session = create_session().object_session(current_user)
        session.add(current_user)
        session.commit()

    change_description_form.description.data = current_user.description

    return render_template("users/profile.html", **data)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
