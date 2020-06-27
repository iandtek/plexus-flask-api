from flask import Flask, json, jsonify
import time
from .youtube_api import save_data
from flask_cors import CORS, cross_origin

last_time_updated = time.strftime("%A, %d. %B %Y %I:%M:%S %p")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def api():
    with open('plexus.json', 'r') as file_data:
        json_data = json.load(file_data)
    return jsonify(json_data)


@app.route("/sync")
def sync():
    last_time_updated = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    save_data()
    return "Synchronization Complete"


@app.route("/last")
def last():
    return last_time_updated
