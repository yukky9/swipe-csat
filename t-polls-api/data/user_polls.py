import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class UserPoll(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user_polls'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), primary_key=True)
    poll_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("polls.id"), primary_key=True)
    criterion_name_1 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    criterion_rating_1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    criterion_name_2 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    criterion_rating_2 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    criterion_name_3 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    criterion_rating_3 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    checking_question = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    checking_result = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
