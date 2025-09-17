from flask import request
from flask_restful import Resource, abort

from data import db_session
from data.users import User


class ProfileResource(Resource):
    @staticmethod
    def post():
        id_ = str(request.json["id"])
        username = request.json["username"]
        session = db_session.create_session()
        user = session.query(User).filter(User.id == id_).first()
        if user:
            return "OK", 200
        user = User(
            id=id_,
            username=username
        )
        session.add(user)
        session.commit()
        return "OK", 200

    @staticmethod
    def get():
        user_id = request.args.get("id")
        session = db_session.create_session()
        user_polls_amount = session.query(User.polls_amount).filter(User.id == user_id).first()
        if not user_polls_amount:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        return {"polls_amount": user_polls_amount[0]}, 200


class UserResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("id")
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"response": 0}, 200
        return {"response": 1}, 200


class SettingsResource(Resource):
    @staticmethod
    def put():
        user_id = str(request.json["id"])
        light_theme = request.json["light_theme"]
        swipe_mode = request.json["swipe_mode"]
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найдено")
        user.light_theme = light_theme
        user.swipe_mode = swipe_mode
        session.commit()
        return "OK", 200

    @staticmethod
    def get():
        user_id = str(request.args.get("id"))
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        return {"light_theme": user.light_theme, "swipe_mode": user.swipe_mode}, 200
