from flask import url_for
from sqlalchemy import (
    Integer,
    String,
    Column,
)
from sqlalchemy.orm import relationship

from .abstract import Model
from .core import Serializable
from .db_session import SqlAlchemyBase
from ..utils.utils import img_url


class ItemType(Model, SqlAlchemyBase):
    __tablename__ = "item_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    rare = Column(Integer)

    def create(self):
        from .item import Item

        item = Item()
        item.item_type = self

        return item

    @property
    def url(self):
        return f"/item_type/{self.id}"

    @property
    def img_url(self):
        return img_url(self.image)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": url_for("static", filename=self.image),
            "rare": self.rare,
        }
