from flask import request
from flask_restful import Resource, abort

from misc import generate_criteria


class CriteriaResource(Resource):
    @staticmethod
    def get():
        name = request.args.get("name")
        if name is None:
            abort(404, message="Имя является объектом None")
        try:
            return generate_criteria(name)
        except Exception as e:
            abort(404, message=f"Ошибка при генерации: {e}")
            raise
