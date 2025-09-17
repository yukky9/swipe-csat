from flask import request
from flask_restful import Resource, abort

from misc import generate_analysis


class AnalysisResource(Resource):
    @staticmethod
    def get():
        name = request.args.get("name")
        if name is None:
            abort(404, message="Имя является объектом None")
        criteria = request.args.get("criteria")
        if criteria is None:
            abort(404, message="Критерии являются объектом None")
        try:
            return generate_analysis(name, criteria)
        except Exception as e:
            abort(404, message=f"Ошибка при генерации: {e}")
            raise
