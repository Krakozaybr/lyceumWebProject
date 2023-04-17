from flask import url_for
from sqlalchemy import (
    Integer,
    String,
    Column,
)

from .core import Serializable
from .db_session import SqlAlchemyBase


class ItemType(SqlAlchemyBase, Serializable):
    __tablename__ = "item_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    image = Column(String)
    rare = Column(Integer)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": url_for("static", filename=self.image),
            "rare": self.rare,
        }
