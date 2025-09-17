import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Criterion(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'criteria'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    poll_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("polls.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    one_point_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    two_points_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    three_points_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    four_points_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    five_points_amount = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    csat = sqlalchemy.Column(sqlalchemy.Integer, default=0)
