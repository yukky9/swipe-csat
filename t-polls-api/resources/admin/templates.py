from flask import request
from flask_restful import Resource, abort

from data import db_session
from data.templates import Template
from data.template_criteria import TemplateCriteria

from gateway import generate_criteria


class TemplatesResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        templates = session.query(Template).all()
        res = []
        for template in templates:
            res.append(template.to_dict(only=("id", "name")))
        return res, 200


class TemplateResource(Resource):
    @staticmethod
    def post():
        name = request.json["name"]
        criteria = request.json["criteria"].split(",")
        unique_criteria = set(criteria)
        if len(unique_criteria) != len(criteria):
            abort(400, message="Критерии повторяются")
        session = db_session.create_session()
        template = Template(
            name=name
        )
        session.add(template)
        session.commit()
        for i in range(len(criteria)):
            template_criteria = TemplateCriteria(
                template_id=template.id,
                name=criteria[i]
            )
            session.add(template_criteria)
            session.commit()
        return "OK", 200

    @staticmethod
    def put():
        template_id = request.json["id"]
        name = request.json.get("name")
        criteria = request.json.get("criteria")
        if criteria is not None:
            criteria.split(",")
            unique_criteria = set(criteria)
            if len(unique_criteria) != len(criteria):
                abort(400, message="Критерии повторяются")
        session = db_session.create_session()
        template = session.query(Template).filter(Template.id == template_id).first()
        if not template:
            abort(404, message=f"Опрос с ID [{template_id}] не найден")
        if name is not None and name != template.name:
            template.name = name
        session.commit()
        session.query(TemplateCriteria).filter(TemplateCriteria.template_id == template_id).delete()
        session.commit()
        if criteria is not None:
            for i in range(len(criteria)):
                template_criteria = TemplateCriteria(
                    template_id=template.id,
                    name=criteria[i]
                )
                session.add(template_criteria)
                session.commit()
        return "OK", 200

    @staticmethod
    def get():
        template_id = request.args.get("id")
        session = db_session.create_session()
        template = session.query(Template).filter(Template.id == template_id).first()
        if not template:
            abort(404, message=f"Опрос с ID [{template_id}] не найден")
        res = {"name": template.name}
        template_criteria = session.query(TemplateCriteria).filter(TemplateCriteria.template_id == template_id).all()
        for criterion in template_criteria:
            res[criterion.id] = criterion.name
        return res, 200

    @staticmethod
    def delete():
        template_id = request.args.get("id")
        session = db_session.create_session()
        template = session.query(Template).filter(Template.id == template_id).first()
        if not template:
            abort(404, message=f"Опрос с ID [{template_id}] не найден")
        session.query(TemplateCriteria).filter(TemplateCriteria.template_id == template_id).delete()
        session.delete(template)
        session.commit()
        return "OK", 200


class GeneratedTemplateResource(Resource):
    @staticmethod
    def get():
        name = request.args.get("name")
        if name is None:
            abort(400, message="Не указано имя шаблона")
        try:
            return generate_criteria(name).split(", "), 200
        except Exception as e:
            abort(400, message=f"Ошибка при генерации: {e}")
