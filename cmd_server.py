import os
import json
import time
from bottle import run, post, request, response, HTTPResponse

q = None
RSP_TO = 5
CHECK_TIM = 0.2

@post('/voice_command')
def command_handler():
    global q
    j = {
            "type": "voice",
            "content": request.body.read().decode()
    }
    q.put(json.dumps(j, indent=2))


@post('/scan_result')
def command_handler():
    global q
    j = {
            "type": "scan",
            "content": request.body.read().decode()
    }
    q.put(json.dumps(j, indent=2))


def run_server(queue):
    global q
    try:
        q = queue
        run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        exit(0)


