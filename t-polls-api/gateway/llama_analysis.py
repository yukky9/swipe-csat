import json
import requests


def generate_analysis(name, criteria):
    params = {
        "name": name,
        "criteria": criteria
    }
    llama_api_server = "http://kowlad123321456654.tplinkdns.com/api/llama/analysis"
    req = requests.get(llama_api_server, params=params, timeout=300)
    req = json.loads(req.content)
    return req
