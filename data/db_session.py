import logging

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()


def global_init(*args, **kwargs) -> Session:
    db_engine, db_user, db_password, db_host, db_port, db_name = kwargs.values()

    if not db_name or not db_name.strip():
        raise Exception("Необходимо указать файл базы данных.")

    sqlalchemy_database_url = '{}://{}:{}@{}:{}/{}'.format(
        db_engine, db_user, db_password, db_host, db_port, db_name)
    logging.debug(
        f"Подключение к базе данных по адресу {sqlalchemy_database_url}")

    engine = sa.create_engine(sqlalchemy_database_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)
    return __factory()


# def create_session() -> Session:
#     global __factory
#     return __factory()
