from sqlalchemy import Integer, String, Column, ForeignKey, Table, orm

from .core import Serializable
from .db_session import SqlAlchemyBase


class Chest(SqlAlchemyBase, Serializable):
    __tablename__ = "chests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    items_count_min = Column(Integer)
    items_count_max = Column(Integer)
    coins_min = Column(Integer)
    coins_max = Column(Integer)

    item_types = orm.relationship(
        "ItemType", secondary="chests_to_item_types", back_populates="chests"
    )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "items_count_min": self.items_count_min,
            "items_count_max": self.items_count_max,
            "coins_min": self.coins_min,
            "coins_max": self.coins_max,
        }


association_table = Table(
    "chests_to_item_types",
    SqlAlchemyBase.metadata,
    Column("chests", Integer, ForeignKey("chests.id")),
    Column("item_types", Integer, ForeignKey("item_types.id")),
)
