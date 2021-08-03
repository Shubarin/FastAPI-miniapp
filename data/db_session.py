import logging

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()


def global_init(*args, **kwargs) -> Session:
    """
    Initializes a session in the database.
    Adds new models when the app is launched for the first time.
    :param args:
    :param kwargs:
    :return:
    """
    db_engine, db_user, db_password, db_host, db_port, db_name = kwargs.values()

    if not db_name or not db_name.strip():
        raise Exception("Please specify the name of the database.")

    sqlalchemy_database_url = '{}://{}:{}@{}:{}/{}'.format(
        db_engine, db_user, db_password, db_host, db_port, db_name)
    logging.debug(
        f"Connect to database {sqlalchemy_database_url}")

    engine = sa.create_engine(sqlalchemy_database_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)
    return __factory()


# def create_session() -> Session:
#     global __factory
#     return __factory()
