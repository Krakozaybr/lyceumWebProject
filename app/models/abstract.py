from app.models.core import Serializable


class Model(Serializable):
    def save_model(self, session):

        session.add(self)
        session.commit()
        session.refresh(self)
