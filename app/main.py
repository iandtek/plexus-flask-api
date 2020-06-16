from flask import Flask, json, jsonify
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from .youtube_api import save_data
from flask_cors import CORS, cross_origin

last_time_updated = time.strftime("%A, %d. %B %Y %I:%M:%S %p")


def update_database():
    last_time_updated = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    save_data()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_database, trigger="interval", hours=0.5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/api.json")
@cross_origin()
def api():
    with open('plexus.json', 'r') as file_data:
        json_data = json.load(file_data)
    return jsonify(json_data)


@app.route("/last")
def last():
    return last_time_updated


@app.route("/sync")
def sync():
    save_data()
    return "Synchronization Complete"
