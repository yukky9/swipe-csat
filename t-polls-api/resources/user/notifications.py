import datetime
from flask_restful import Resource
from data import db_session
from data.users import User
from data.notifications import Notification


class NotificationsResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        time_stamp = datetime.datetime.now() - datetime.timedelta(hours=23, minutes=59)
        print(time_stamp)
        users = session.query(User).all()
        notifications = session.query(Notification).filter(Notification.time > time_stamp).all()
        if not notifications:
            return [], 200
        res = []
        for user in users:
            d = {"id": user.id}
            print(user.last_request > time_stamp)
            if user.last_request > time_stamp:
                time_stamp = user.last_request
                print(time_stamp)
            ll = []
            notifications = session.query(Notification).filter(Notification.time > time_stamp).all()
            print(notifications)
            for notification in notifications:
                if user.id not in notification.stampiks.split(","):
                    ll.append(notification.name)
                    notification.stampiks += f"{user.id},"
            d["notifications"] = ll
            res.append(d)
        return res, 200
