from flask import Flask, request, jsonify
from agent import CodingAgent
from db import init_db
from flask_cors import CORS
from tools import code_exec

app = Flask(__name__)
CORS(app)
init_db()
agent = CodingAgent()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    answer = agent.handle_request(prompt)
    clean_code = code_exec.extract_code(answer)
    return jsonify({"code": clean_code})

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    code = data.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    result = agent.run_code(code)
    return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
