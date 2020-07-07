from flask import Flask, json, jsonify, request
import time
from .youtube_api import save_data
from flask_cors import CORS, cross_origin
import requests

last_time_updated = time.strftime("%A, %d. %B %Y %I:%M:%S %p")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/api.json")
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


@app.route("/order", methods=['POST'])
def order():
    url = 'http://andtek.ddns.net:3000/api/v1/jobs'
    raw = json.loads(request.form.get('rawRequest'))

    order = {
        "user": raw['q3_email3'],
        "template": {
            "src": "file:///E:/nexrender/chromatic.aep",
            "composition": "720p"
        },
        "assets": [
            {
                "src": raw['logo'][0],
                "type": "image",
                "layerName": "logo"
            },
            {
                "type": "data",
                "layerName": "logo",
                "property": "Scale",
                "expression": "h = (thisComp.height/height)*100; w = (thisComp.width/width)*100; if(w > h) {[h,h]} else {[w,w]}"
            },
            {
                "type": "data",
                "layerName": "page",
                "property": "Source Text",
                "value": raw['q17_webpage']
            }
        ],
        "actions": {
            "postrender": [
                {
                    "module": "@nexrender/action-encode",
                    "preset": "mp4",
                    "output": "encoded.mp4",
                    "params": {"-vcodec": "libx264", "-r": 25}
                },
                {
                    "module": "@nexrender/action-copy",
                    "input":  "encoded.mp4",
                    "output": "e:/Nexrender/Lookout 2.mp4"
                },
                {
                    "module": "nexrender-action-cloudinary",
                    "input": "encoded.mp4",
                    "params": {
                        "api_key": "545734925218622",
                        "cloud_name": "dvwbenmc8",
                        "api_secret": "BLEz7MHdcna5-gdPbIHore07EYM",
                        "UploadApiOptions": {
                            "resource_type": "video"
                        }
                    }
                }
            ]
        }
    }
    print(order)
    x = requests.post(url, json=order)
    return x.text
