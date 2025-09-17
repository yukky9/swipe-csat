import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class TemplateCriteria(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'template_criteria'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    template_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("templates.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
