from datetime import datetime

from flask import url_for
from sqlalchemy import Integer, String, Column, DateTime, Boolean

from app.models.core import Serializable, format_date
from app.models.db_session import SqlAlchemyBase
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, Serializable):

    __tablename__ = "users"

    DEFAULT_AVATAR = "default_avatar.png"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    description = Column(String, default="")
    bill = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_staff = Column(Boolean, default=False)
    avatar = Column(String, default="")

    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": self.id,
            "login": self.login,
            "password": self.password,
            "description": self.description,
            "bill": self.bill,
            "created_at": format_date(self.created_at),
            "is_staff": self.is_staff,
        }

    @property
    def img_url(self):
        img = self.avatar or self.DEFAULT_AVATAR
        return url_for("static", filename=f"images/{img}")

    @property
    def preview_url(self):
        return f'/users/{self.id}'
