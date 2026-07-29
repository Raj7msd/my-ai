from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)

# OpenRouter API Key
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message received"}), 400

    try:
        response = client.chat.completions.create(
            model="poolside/laguna-xs-2.1:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Your name is My-AI. "
                        "You are a highly advanced and smart AI assistant. "
                        "You were created, developed and founded by Raj (Raj Divakar). "
                        "If anyone asks your creator, founder or developer, always answer Raj. "
                        "Be friendly, logical, technical and helpful. "
                        "If the user asks programming questions, teach like a professional software engineer in simple language. "
                        "Use emojis naturally."
                    ),
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
        )

        ai_reply = response.choices[0].message.content

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"reply": f"Backend Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)


