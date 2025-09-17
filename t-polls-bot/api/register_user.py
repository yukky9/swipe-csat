import requests
import config


def register_user(username, user_id):
    req = requests.post(config.API + "/api/user/profile", json={"username": username, "id": user_id})
    if req.status_code != 200:
        raise requests.exceptions.RequestException
