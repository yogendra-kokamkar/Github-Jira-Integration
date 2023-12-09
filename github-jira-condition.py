from flask import Flask, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)

@app.route("/createJIRA", methods=['POST'])
def createJIRA():
    webhook = request.json
    print(webhook)
    url = "https://<username>.atlassian.net/rest/api/3/issue"

    auth = HTTPBasicAuth("email@example.com", "<APIToken>")

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = json.dumps( {
    "fields": {
        "description": {
        "content": [
            {
            "content": [
                {
                "text": "GitHub Issue Commented.",
                "type": "text"
                }
            ],
            "type": "paragraph"
            }
        ],
        "type": "doc",
        "version": 1
        },
        "issuetype": {
        "id": "10006"
        },
        "project": {
        "key": "YOG"
        },
        "summary": "Github issue comment added",
    },
    "update": {}
    } )
    response = None
    if webhook['comment'].get('body') == "/jira":
        response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
        return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    else:
        print('Jira issue will be created if comment include /jira')

app.run('0.0.0.0', port=5000)
