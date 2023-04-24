import datetime

from sqlalchemy import (
    Integer,
    String,
    Column,
    orm,
    ForeignKey,
    DateTime,
)

from .abstract import Model
from .core import format_date
from .db_session import SqlAlchemyBase


class Product(Model, SqlAlchemyBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_description = Column(String)
    price = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    count = Column(Integer)
    item_type_id = Column(Integer, ForeignKey("item_types.id"))

    item_type = orm.relationship("ItemType")
    user = orm.relationship("User", backref="products")

    @property
    def url(self):
        return f"/product/{self.id}"

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
