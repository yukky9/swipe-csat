import datetime
from flask import request
from flask_restful import Resource, abort

from data import db_session
from data.polls import Poll
from data.user_polls import UserPoll
from data.criteria import Criterion
from data.special import Special
from data.notifications import Notification
from gateway import generate_analysis


class AdminPollsResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        polls = session.query(Poll).all()
        return [poll.to_dict(only=("id", "name", "description", "date", "respondent_amount", "rating"))
                for poll in polls], 200


class AdminPollResource(Resource):
    @staticmethod
    def post():
        name = request.json["name"]
        description = request.json["description"]
        criteria = request.json["criteria"].split(",")
        unique_criteria = set(criteria)
        if len(unique_criteria) != len(criteria):
            abort(400, message="Критерии повторяются")
        question = request.json["question"]
        answer = request.json["answer"]
        session = db_session.create_session()
        poll = Poll(
            name=name,
            description=description,
            date=datetime.datetime.utcnow()
        )
        session.add(poll)
        for i in range(len(criteria)):
            poll.criteria.append(Criterion(name=criteria[i], poll_id=poll.id))
        poll.special.append(Special(question=question, answer=answer, poll_id=poll.id))
        session.commit()
        print(datetime.datetime.utcnow())
        notification = Notification(
            id=poll.id,
            name=poll.name,
            time=datetime.datetime.utcnow()
        )
        session.add(notification)
        session.commit()
        return "OK", 200

    @staticmethod
    def put():
        poll_id = request.json["id"]
        name = request.json.get("name")
        description = request.json.get("description")
        criteria = request.json.get("criteria")
        if criteria is not None:
            criteria = criteria.split(",")
            unique_criteria = set(criteria)
            if len(unique_criteria) != len(criteria):
                abort(400, message="Критерии повторяются")
        question = request.json.get("question")
        answer = request.json.get("answer")
        session = db_session.create_session()
        poll = session.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            abort(404, message=f"Опрос с ID [{poll_id}] не найден")
        if name is not None and name != poll.name:
            poll.name = name
        if description is not None and description != poll.description:
            poll.description = description
        if criteria is not None:
            prev_criteria = session.query(Criterion.name).filter(Criterion.poll_id == poll_id).all()
            change_rating = False
            for i in range(len(criteria)):
                criterion = criteria[i].split(";")
                if int(criterion[0]) in prev_criteria:
                    if criterion[1] != prev_criteria[prev_criteria.index(int(criterion[0]))]:
                        poll.criteria[prev_criteria.index(int(criterion[0]))].name = criterion[1]
                else:
                    poll.criteria.append(Criterion(name=criterion[1], poll_id=poll_id))
                    change_rating = True
            session.commit()
            if change_rating:
                criteria_csat = session.query(Criterion.csat).filter(Criterion.poll_id == poll_id).all()
                s = 0
                for i in range(len(criteria_csat)):
                    s += int(criteria_csat[i][0])
                poll.rating = round(s / len(criteria_csat))
                session.commit()
        if question is not None or answer is not None:
            special = session.query(Special).filter(Special.poll_id == poll_id).first()
            if not special:
                abort(404, message=f"Специальная информация для опроса с ID [{poll_id}] не найдена")
            if question is not None and special.question != question:
                special.question = question
            if answer is not None and special.answer != answer:
                special.answer = answer
            session.commit()
        return "OK", 200

    @staticmethod
    def get():
        poll_id = request.args.get("id")
        session = db_session.create_session()
        poll = session.query(Poll).filter(Poll.id == poll_id).first()
        if not poll:
            abort(404, message=f"Опрос с ID [{poll_id}] не найден")
        special = session.query(Special).filter(Special.poll_id == poll_id).first()
        if not special:
            abort(404, message=f"Специальная информация для опроса с ID [{poll_id}] не найдена")
        criteria_res = []
        for_gen_criteria = []
        for criterion in poll.criteria:
            criteria_res.append({
                "criteria_id": criterion.id,
                "criteria_name": criterion.name,
                "csat": criterion.csat
            })
            for_gen_criteria.append(f"{criterion.name}: {criterion.csat}")
        try:
            generated_offer = generate_analysis(poll.name, ", ".join(for_gen_criteria))
        except Exception as e:
            generated_offer = f"Ошибка во время генерации: {e}"
        res = {
            "id": poll.id,
            "name": poll.name,
            "description": poll.description,
            "rating": poll.rating,
            "offer": generated_offer,
            "question": special.question,
            "answer": special.answer,
            "criteria": criteria_res
        }
        return res, 200

    @staticmethod
    def delete():
        poll_id = request.args.get("id")
        session = db_session.create_session()
        session.query(UserPoll).filter(UserPoll.poll_id == poll_id).delete()
        session.query(Notification).filter(Notification.id == poll_id).delete()
        session.query(Criterion).filter(Criterion.poll_id == poll_id).delete()
        session.query(Special).filter(Special.poll_id == poll_id).delete()
        session.query(Poll).filter(Poll.id == poll_id).delete()
        session.commit()
        return "OK", 200
