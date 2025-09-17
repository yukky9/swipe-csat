import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Special(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'special'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    poll_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("polls.id"))
    question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
