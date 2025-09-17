from flask import Flask
from flask_restful import Api
from flask_cors import CORS
# from flask_ngrok import run_with_ngrok

from resources import *
from data import db_session
from config import RUN_WITH_NGROK, DEBUG, SECRET_KEY, ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH, DATABASE_URL


app = Flask(__name__)
CORS(app, supports_credentials=True)


# run_with_ngrok(app) if RUN_WITH_NGROK else None

app.config.update({
    "SECRET_KEY": SECRET_KEY,
    "JSON_AS_ASCII": False,
    "UPLOAD_FOLDER": "assets",
    "MAX_CONTENT_LENGTH": MAX_CONTENT_LENGTH,
    "ALLOWED_EXTENSIONS": ALLOWED_EXTENSIONS,
})


@app.route("/")
def check_work():
    return "OK"


db_session.global_init(DATABASE_URL)


api = Api(app)
api.add_resource(AdminPollsResource, "/api/admin/polls")
api.add_resource(AdminPollResource, "/api/admin/poll")
api.add_resource(TemplatesResource, "/api/admin/templates")
api.add_resource(TemplateResource, "/api/admin/template")
api.add_resource(GeneratedTemplateResource, "/api/admin/generated_template")

api.add_resource(HistoriesResource, "/api/user/histories")
api.add_resource(HistoryResource, "/api/user/history")
api.add_resource(NotificationsResource, "/api/user/notifications")
api.add_resource(UserPollsResource, "/api/user/polls")
api.add_resource(UserPollResource, "/api/user/poll")
api.add_resource(UserSwipePollResource, "/api/user/swipe")
api.add_resource(ProfileResource, "/api/user/profile")
api.add_resource(UserResource, "/api/user/check_user")
api.add_resource(SettingsResource, "/api/user/settings")


def main():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
