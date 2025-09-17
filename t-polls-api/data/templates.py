import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Template(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'templates'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    template_criteria = orm.relationship(
        "TemplateCriteria",
        backref="templates"
    )
