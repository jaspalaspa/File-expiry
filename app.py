from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load codes from files.json
def load_codes():
    with open("files.json", "r") as f:
        return json.load(f)

@app.route("/validate", methods=["GET"])
def validate():
    code = request.args.get("code")
    user_id = request.args.get("user_id")

    if not code:
        return jsonify({"valid": False, "error": "Code missing"}), 400

    codes = load_codes()
    if code not in codes:
        return jsonify({"valid": False, "error": "Invalid code"}), 404

    entry = codes[code]

    # Expiry check
    try:
        expiry = datetime.strptime(entry["expiry"], "%Y-%m-%d")
    except Exception:
        return jsonify({"valid": False, "error": "Invalid expiry date format"}), 400

    if datetime.now() > expiry:
        return jsonify({"valid": False, "error": f"Code expired on {entry['expiry']}"}), 403

    # User check
    if entry["user_id"] != "all" and entry["user_id"] != user_id:
        return jsonify({"valid": False, "error": "Not allowed for this user"}), 403

    return jsonify({"valid": True}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
