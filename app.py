# app.py

from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# הגדרות — תמלא את הערכים שלך בקובץ .env או ישירות כאן
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "הכנס_כאן_את_המפתח")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")  # לדוגמה: gpt-4 או gpt-3.5-turbo
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))  # ערך בין 0 ל-1

# יצירת לקוח OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": user_message}],
            temperature=OPENAI_TEMPERATURE,
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "הבוט פועל ✅. שלח POST אל /chat עם הודעה."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
