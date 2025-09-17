import json
import requests


def generate_criteria(name):
    params = {
        "name": name,
    }
    llama_api_server = "http://kowlad123321456654.tplinkdns.com/api/llama/criteria"
    req = requests.get(llama_api_server, params=params, timeout=300)
    req = json.loads(req.content)
    return req
