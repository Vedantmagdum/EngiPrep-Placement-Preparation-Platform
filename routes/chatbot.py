
from flask import Blueprint, request, jsonify, session
from api_service import chat_with_gemini

chatbot = Blueprint("chatbot", __name__)

MAX_MESSAGE_LENGTH = 2000
MAX_HISTORY_ITEMS = 10


@chatbot.route("/chatbot", methods=["POST"])
def chatbot_reply():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "")

    if not isinstance(message, str):
        return jsonify({
            "reply": "Please enter a valid message."
        }), 400

    message = message.strip()

    if not message:
        return jsonify({
            "reply": "Please type a message first."
        }), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "reply": "Please keep your message under 2000 characters."
        }), 400

    history = data.get("history", [])

    if not isinstance(history, list):
        history = []

    safe_history = []

    for item in history[-MAX_HISTORY_ITEMS:]:

        if not isinstance(item, dict):
            continue

        role = item.get("role")
        text = item.get("text", "")

        if (
            role in ("user", "assistant")
            and isinstance(text, str)
            and text.strip()
        ):
            safe_history.append({
                "role": role,
                "text": text[:2000]
            })

    try:

        reply = chat_with_gemini(
            message,
            safe_history
        )

        return jsonify({
            "reply": reply
        })

    except Exception as error:

        print("Chatbot error:", error)

        return jsonify({
            "reply": "I'm having trouble responding right now. Please try again in a moment."
        }), 500
