from flask import Flask, request, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)

DATA_FILE = "files.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/check", methods=["GET"])
def check_file():
    filename = request.args.get("file")
    data = load_data()

    if filename not in data:
        return jsonify({"status": "error", "message": "File not found"}), 404

    expiry_str = data[filename]["expiry"]
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")

    if datetime.now() > expiry_date:
        return jsonify({"status": "expired"})
    else:
        return jsonify({"status": "valid"})

@app.route("/add", methods=["POST"])
def add_file():
    req_data = request.json
    filename = req_data["file"]
    expiry = req_data["expiry"]

    data = load_data()
    data[filename] = {"expiry": expiry}
    save_data(data)

    return jsonify({"status": "success", "message": "File added"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
