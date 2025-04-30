from flask import Flask, request, jsonify, send_from_directory
import openai
import os

app = Flask(__name__, static_folder='')

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content
        return jsonify({'reply': reply.strip()})
    except Exception as e:
        return jsonify({'reply': f'שגיאה: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
