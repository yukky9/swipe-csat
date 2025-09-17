from flask import request
from flask_restful import Resource, abort

from data import db_session
from data.polls import Poll
from data.user_polls import UserPoll


class HistoriesResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("id")
        session = db_session.create_session()
        user_polls = session.query(UserPoll).filter(UserPoll.user_id == user_id).all()
        if not user_polls:
            return [], 200
        res = []
        for i in range(len(user_polls)):
            poll = session.query(Poll).filter(Poll.id == user_polls[i].poll_id).first()
            if not poll:
                abort(404, message=f"Опрос с ID [{user_polls[i].poll_id}] пользователя с ID [{user_id}] не найден")
            res.append(poll.to_dict(only=("id", "name", "description")))
        return res, 200


class HistoryResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("user_id")
        poll_id = request.args.get("poll_id")
        session = db_session.create_session()
        user_poll = session.query(UserPoll).filter(UserPoll.user_id == user_id, UserPoll.poll_id == poll_id).first()
        if not user_poll:
            abort(404, message=f"Опрос с ID [{poll_id}] пользователя с ID [{user_id}] не найден")
        res = {
            "criterion_name_1": user_poll.criterion_name_1, "criterion_rating_1": user_poll.criterion_rating_1,
            "criterion_name_2": user_poll.criterion_name_2, "criterion_rating_2": user_poll.criterion_rating_2,
            "criterion_name_3": user_poll.criterion_name_3, "criterion_rating_3": user_poll.criterion_rating_3,
            "question": user_poll.checking_question, "answer": user_poll.checking_result
        }
        return res, 200
