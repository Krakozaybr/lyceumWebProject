import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import logging as log
import weakref

SqlAlchemyBase = dec.declarative_base()

__factory = None


class CarefulSession(orm.Session):
    def add(self, object_):
        # Get the session that contains the object, if there is one.
        object_session = orm.object_session(object_)
        if object_session and object_session is not self:
            # Remove the object from the other session, but keep
            # a reference so we can reinstate it.
            object_session.expunge(object_)
            object_._prev_session = weakref.ref(object_session)
        return super().add(object_)


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    log.info(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(engine, class_=CarefulSession)

    @sa.event.listens_for(__factory, "after_commit")
    def receive_after_commit(session):
        """Reinstate objects into their previous sessions."""
        objects = filter(
            lambda o: hasattr(o, "_prev_session"), session.identity_map.values()
        )
        for object_ in objects:
            prev_session = object_._prev_session()
            if prev_session:
                session.expunge(object_)
                prev_session.add(object_)
                delattr(object_, "_prev_session")

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
