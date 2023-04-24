from random import choices, randint

from sqlalchemy import Integer, String, Column, ForeignKey, Table, orm

from .abstract import Model
from .db_session import SqlAlchemyBase
from ..utils.utils import img_url


class Chest(Model, SqlAlchemyBase):
    __tablename__ = "chests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    image = Column(String)
    description = Column(String)
    items_count_min = Column(Integer)
    items_count_max = Column(Integer)
    coins_min = Column(Integer)
    coins_max = Column(Integer)
    price = Column(Integer)

    item_types = orm.relationship(
        "ItemType", secondary="chests_to_item_types", backref="chests"
    )

    def open(self, user: "User", session):
        from .transaction import Transaction

        coins = randint(self.coins_min, self.coins_max)
        count = randint(self.items_count_min, self.items_count_max)

        population = []
        weights = []

        for item_type in self.item_types:
            population.append(item_type)
            weights.append(1 / item_type.rare)

        items = []
        for item_type in list(choices(population, weights, k=count)):
            item = item_type.create()
            items.append(item)

        transaction = Transaction()
        transaction.to_user = user
        transaction.items.extend(items)
        transaction.money = self.price - coins
        transaction.apply(session)

        session.commit()
        session.refresh(transaction)

        return transaction

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

    @property
    def img_url(self):
        return img_url(self.image)

    @property
    def url(self):
        return f"/chest/{self.id}"


association_table = Table(
    "chests_to_item_types",
    SqlAlchemyBase.metadata,
    Column("chests", Integer, ForeignKey("chests.id")),
    Column("item_types", Integer, ForeignKey("item_types.id")),
)
