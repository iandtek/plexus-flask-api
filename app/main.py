from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/inventory")
def home_view():
    with open('plexus.json', 'r') as file_data:
        json_data = json.load(file_data)
    return jsonify(json_data)
