import datetime

from sqlalchemy import Integer, String, Column, orm, ForeignKey, DateTime

from .abstract import Model
from .db_session import SqlAlchemyBase


class Comment(Model, SqlAlchemyBase):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    date = Column(DateTime, default=datetime.datetime.now)

    user = orm.relationship("User", backref="comments")
    target = orm.relationship("Product", backref="comments")

    def to_json(self):
        return {
            "id": self.id,
            "target_id": self.target_id,
            "user": self.user.to_json(),
            "text": self.text,
        }
