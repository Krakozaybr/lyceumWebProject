import datetime

from sqlalchemy import (
    Integer,
    Column,
    orm,
    ForeignKey,
    DateTime,
    Boolean,
    Table,
)

from .abstract import Model
from .core import format_date
from .db_session import SqlAlchemyBase
from ..utils.models_utils import items_to_dict


class Transaction(Model, SqlAlchemyBase):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(DateTime, default=datetime.datetime.now)
    money = Column(Integer, default=0)
    is_applied = Column(Boolean)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    to_user = orm.relationship(
        "User", backref="income_transactions", foreign_keys="Transaction.to_user_id"
    )
    from_user = orm.relationship(
        "User", backref="outcome_transactions", foreign_keys="Transaction.from_user_id"
    )

    items = orm.relationship(
        "Item", secondary="transactions_to_items", backref="transactions"
    )

    @property
    def items_dict(self):
        return items_to_dict(self.items)

    def apply(self, session):
        self.is_applied = True
        if self.from_user:
            self.from_user.bill += self.money
            session.add(self.from_user)
        if self.to_user:
            self.to_user.bill -= self.money
            session.add(self.to_user)
        for item in self.items:
            item.user = self.to_user
            session.add(item)
        session.add(self)

    def to_json(self):
        return {
            "id": self.id,
            "created_at": format_date(self.created_at),
            "is_applied": self.is_applied,
            "to_user_id": self.to_user_id,
            "from_user_id": self.from_user_id,
        }

    @property
    def url(self):
        return f"/transaction/{self.id}"


association_table = Table(
    "transactions_to_items",
    SqlAlchemyBase.metadata,
    Column("transactions", Integer, ForeignKey("transactions.id")),
    Column("items", Integer, ForeignKey("items.id")),
)
