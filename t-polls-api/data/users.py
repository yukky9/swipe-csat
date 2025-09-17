import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, default="t-user")
    polls_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    light_theme = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    swipe_mode = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    last_request = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)

    polls = orm.relationship(
        "Poll",
        secondary="user_polls",
        backref="users"
    )
