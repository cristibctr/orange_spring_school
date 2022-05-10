import json
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)
with open('api.key') as f:
    password = f'{f.read()}'

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/v0/devices")
def list_devices():
    Headers = {
        'X-Api-Key': password,
    }
    myRequest = requests.get(
        'https://liveobjects.orange-business.com/api/v1/deviceMgt/devices', headers=Headers)
    responseObj = json.loads(myRequest.content)
    return jsonify(responseObj)


@app.route("/api/v0/stream/<device_id>")
def list_streams(device_id):
    Headers = {
        'X-Api-Key': password,
    }
    myRequest = requests.get(
        f'https://liveobjects.orange-business.com/api/v1/deviceMgt/devices/{device_id}/data/streams', headers=Headers)
    responseObj = json.loads(myRequest.content)
    return jsonify(responseObj)


@app.route("/api/v0/telemetry/<deviceId>")
def device_telem(deviceId):
    Headers = {
        'X-Api-Key': password,
    }
    myRequest = requests.get(
        f'https://liveobjects.orange-business.com/api/v0/data/streams/{deviceId}?limit=1', headers=Headers)
    responseObj = json.loads(myRequest.content)
    return {
        "temperature": responseObj[0]['value']['temperature'],
        "humidity": responseObj[0]['value']['hygrometry'],
        "pressure": responseObj[0]['value']['pressure'],
        "CO2": responseObj[0]['value']['CO2']
    }
