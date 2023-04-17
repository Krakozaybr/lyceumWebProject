from sqlalchemy import Integer, Column, orm, ForeignKey

from .core import Serializable
from .db_session import SqlAlchemyBase


class Item(SqlAlchemyBase, Serializable):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type_id = Column(Integer, ForeignKey("item_types.id"))

    user = orm.relationship("User", back_populates="items")
    item_type = orm.relationship("ItemType")

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type.to_json(),
        }
