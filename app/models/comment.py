from sqlalchemy import Integer, String, Column, orm, ForeignKey

from .core import Serializable
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, Serializable):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    target_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    stars = Column(Integer)

    user = orm.relationship("User", back_populates="comments")
    target = orm.relationship("Product", back_populates="comments")

    def to_json(self):
        return {
            "id": self.id,
            "target_id": self.target_id,
            "user": self.user.to_json(),
            "text": self.text,
            "stars": self.stars,
        }
