from sqlalchemy import Integer, Column, orm, ForeignKey, Boolean

from .abstract import Model
from .core import Serializable
from .db_session import SqlAlchemyBase


class Item(Model, SqlAlchemyBase):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type_id = Column(Integer, ForeignKey("item_types.id"))
    is_free = Column(Boolean, default=True)

    user = orm.relationship("User", backref="items")
    item_type = orm.relationship("ItemType")

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.item_type.to_json(),
        }
