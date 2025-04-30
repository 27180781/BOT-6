from flask import Flask, request, jsonify, render_template, redirect
import openai
import json
import os

app = Flask(__name__)

# טען את ההגדרות
CONFIG_FILE = 'config.json'
def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# טען את המפתח של OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # שים את ה-API Key כסביבה ב-Render

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    config = load_config()
    return render_template('admin.html', config=config)

@app.route('/save_config', methods=['POST'])
def save_config():
    data = request.form.to_dict()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return redirect('/admin')

@app.route('/chat', methods=['POST'])
def chat():
    config = load_config()
    user_message = request.json.get('message')

    try:
        # בניית הפרומפט
        business_info = f"""
        מידע על העסק:
        שם העסק: {config.get('business_name')}
        תיאור: {config.get('business_description')}
        קישור למרכז הידע: {config.get('knowledge_base_link')}
        """

        messages = [
            {"role": "system", "content": business_info},
            {"role": "user", "content": user_message}
        ]

        # בקשה ל-OpenAI
        response = openai.ChatCompletion.create(
            model=config.get('model', 'gpt-3.5-turbo'),
            messages=messages,
            temperature=float(config.get('temperature', 0.7)),
            max_tokens=1000
        )

        reply = response.choices[0].message['content'].strip()
        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'reply': f'שגיאה: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
