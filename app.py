import ast
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("TECHCORP_API_KEY", "")
SECRET_TOKEN = os.environ.get("TECHCORP_SECRET_TOKEN", "")

SYSTEM_PROMPT = os.environ.get("TECHCORP_SYSTEM_PROMPT", "Default assistant role.")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_message = data.get("message", "")
    calc_expr = data.get("calc", "1")
    try:
        calc_result = ast.literal_eval(calc_expr)
    except (ValueError, SyntaxError):
        calc_result = None

    payload = {
        "model": "tinyllama",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    return jsonify({"calc": calc_result, "status": "processed"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
