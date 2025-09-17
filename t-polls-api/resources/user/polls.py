import random
import datetime
from flask import request
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from data.polls import Poll
from data.criteria import Criterion
from data.special import Special
from data.user_polls import UserPoll
from misc import find_nearest_number, tuples_to_ints


class UserPollsResource(Resource):
    @staticmethod
    def get():
        user_id = request.args.get("id")
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        user.last_request = datetime.datetime.utcnow()
        session.commit()
        polls = session.query(Poll).all()
        user_polls = tuples_to_ints(session.query(UserPoll.poll_id).filter(UserPoll.user_id == user_id).all())
        res = []
        for poll in polls:
            if poll.id in user_polls:
                continue
            res.append(poll.to_dict(only=("id", "name", "description")))
        return res, 200


class UserPollResource(Resource):
    @staticmethod
    def post():
        user_id = str(request.json["user_id"])
        poll_id = int(request.json["poll_id"])
        criterion_1 = request.json["criterion_1"].split(",")  # name, rating
        criterion_2 = request.json["criterion_2"].split(",")
        criterion_3 = request.json["criterion_3"].split(",")
        criteria = {
            "1": criterion_1,
            "2": criterion_2,
            "3": criterion_3
        }
        special = request.json["special"]
        session = db_session.create_session()
        user_polls = tuples_to_ints(session.query(UserPoll.poll_id).filter(UserPoll.user_id == user_id).all())
        if poll_id in user_polls:
            abort(400, message=f"Пользователь уже прошёл опрос с ID [{poll_id}]")
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message=f"Пользователь с ID [{user_id}] не найден")
        poll = session.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            abort(404, message=f"Опрос с ID [{poll_id}] не найден")
        user.polls_amount += 1
        specials = session.query(Special.question, Special.answer).filter(Special.poll_id == poll_id).first()
        user_poll = UserPoll(
            user_id=user_id,
            poll_id=poll_id,
            criterion_name_1=criteria["1"][0],
            criterion_rating_1=criteria["1"][1],
            criterion_name_2=criteria["2"][0],
            criterion_rating_2=criteria["2"][1],
            criterion_name_3=criteria["3"][0],
            criterion_rating_3=criteria["3"][1],
            checking_question=specials[0],
            checking_result=special
        )
        session.add(user_poll)
        session.commit()
        if special == specials[1]:
            poll.respondent_amount += 1
            for i in range(3):
                criterion = session.query(Criterion).filter(
                    Criterion.poll_id == poll_id,
                    Criterion.name == criteria[str(i + 1)][0]
                ).first()
                if criteria[str(i + 1)][1] == "1":
                    criterion.one_point_amount += 1
                elif criteria[str(i + 1)][1] == "2":
                    criterion.two_points_amount += 1
                elif criteria[str(i + 1)][1] == "3":
                    criterion.three_points_amount += 1
                elif criteria[str(i + 1)][1] == "4":
                    criterion.four_points_amount += 1
                elif criteria[str(i + 1)][1] == "5":
                    criterion.five_points_amount += 1
                criterion.csat = round((criterion.four_points_amount + criterion.five_points_amount) /
                                       (criterion.one_point_amount + criterion.two_points_amount +
                                        criterion.three_points_amount + criterion.four_points_amount +
                                        criterion.five_points_amount) * 100)
                session.commit()
            criteria_csat = session.query(Criterion.csat).filter(Criterion.poll_id == poll_id).all()
            s = 0
            for i in range(len(criteria_csat)):
                s += int(criteria_csat[i][0])
            poll.rating = round(s / len(criteria_csat))
            session.commit()
        return "OK", 200

    @staticmethod
    def get():
        poll_id = request.args.get("id")
        session = db_session.create_session()
        poll = session.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            abort(404, message=f"Опрос с ID [{poll_id}] не найден")
        criteria = session.query(Criterion.id, Criterion.name).filter(Criterion.poll_id == poll_id).all()
        if not criteria:
            abort(404, message=f"Критерий для опроса с ID [{poll_id}] не найден")
        random_criteria = [criteria.pop(random.randrange(len(criteria))) for _ in range(3)]
        if len(random_criteria) != 3:
            abort(404, message=f"Критериев для опроса с ID [{poll_id}] не достаточно")
        special = session.query(Special).filter(Special.poll_id == poll_id).first()
        if not special:
            abort(404, message=f"Специальная информация для опроса с ID [{poll_id}] не найдена")
        res = {
            "id": poll.id, "name": poll.name, "description": poll.description,
            "criteria": [{"id": criteria[0], "name": criteria[1]} for criteria in random_criteria],
            "question": special.question
        }
        return res, 200


class UserSwipePollResource(Resource):
    @staticmethod
    def get():
        prev_poll_id = int(request.args.get("poll_id"))
        user_id = request.args.get("user_id")
        session = db_session.create_session()
        user_polls_ids = session.query(UserPoll.poll_id).filter(UserPoll.user_id == user_id).all()
        poll_prev_ids = session.query(Poll.id).all()
        poll_ids = [int(i[0]) for i in poll_prev_ids if i not in user_polls_ids]
        tmp = find_nearest_number(poll_ids, prev_poll_id)
        if tmp == -1:
            res = {
                "id": -1, "name": "", "description": "",
                "criteria": [{"id": "", "name": ""}],
                "question": ""
            }
            return res, 200
        poll = session.query(Poll).filter(Poll.id == tmp).first()
        criteria = session.query(Criterion.id, Criterion.name).filter(Criterion.poll_id == poll.id).all()
        random_criteria = [criteria.pop(random.randrange(len(criteria))) for _ in range(3)]
        if len(random_criteria) != 3:
            abort(404, message=f"Критериев для опроса с ID [{poll.id}] не достаточно")
        special = session.query(Special).filter(Special.poll_id == poll.id).first()
        res = {
            "id": poll.id, "name": poll.name, "description": poll.description,
            "criteria": [{"id": criteria[0], "name": criteria[1]} for criteria in random_criteria],
            "question": special.question
        }
        return res, 200
