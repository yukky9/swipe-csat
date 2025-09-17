import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Poll(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'polls'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
    respondent_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    criteria = orm.relationship(
        "Criterion",
        backref="polls"
    )

    special = orm.relationship(
        "Special",
        backref="polls"
    )
