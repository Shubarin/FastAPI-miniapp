import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)
import sqlalchemy.ext.declarative as dec
from sqlalchemy.sql import func
from databases import Database

SqlAlchemyBase = dec.declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

images = Table(
    "images",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("original", String),
    Column("negative", String),
    Column("type", String),
    Column("pub_date", DateTime, unique=True, default=func.now()),
)

database = Database(DATABASE_URL)
