import datetime

import sqlalchemy

from .db_session import SqlAlchemyBase


class Image(SqlAlchemyBase):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    original = sqlalchemy.Column(sqlalchemy.String, name='original image')
    negative = sqlalchemy.Column(sqlalchemy.String, name='negative image')
    pub_date = sqlalchemy.Column(sqlalchemy.DateTime, name='pub_date',
                                 unique=True, default=datetime.datetime.utcnow)
    type = sqlalchemy.Column(sqlalchemy.String, name='image type')

    def __repr__(self):
        return f'<Image> {self.id} ({self.pub_date})'
