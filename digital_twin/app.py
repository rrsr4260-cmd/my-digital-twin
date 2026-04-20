from flask import Flask, render_template, request, jsonify
from brain import think
from config import VOICE_OUTPUT
import os

app = Flask(__name__)

os.makedirs("static", exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Kuch to likh bhai.",
                "audio": ""
            })

        reply = think(user_message)

        return jsonify({
            "reply": reply,
            "audio": "/" + VOICE_OUTPUT.replace("\\", "/")
        })

    except Exception as e:
        print("Flask error:", e)
        return jsonify({
            "reply": f"Server error: {str(e)}",
            "audio": ""
        })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)