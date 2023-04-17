from sqlalchemy import (
    Integer,
    String,
    Column,
    orm,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
)

from .core import Serializable, format_date
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, Serializable):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_closed = Column(Boolean)
    count = Column(Integer)
    item_type_id = Column(Integer, ForeignKey("item_types.id"))

    item_type = orm.relationship("ItemType")
    user = orm.relationship("User", back_populates="products")

    def to_json(self):
        return {
            "id": self.id,
            "user_description": self.user_description,
            "price": self.price,
            "created_at": format_date(self.created_at),
            "user_id": self.user.to_json(),
            "is_closed": self.is_closed,
            "count": self.count,
            "item_type": self.item_type.to_json(),
        }
