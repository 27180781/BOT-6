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

        # יצירת אינסטנס של OpenAI Client
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # בקשה ל-OpenAI
        response = client.chat.completions.create(
            model=config.get('model', 'gpt-4'),
            messages=messages,
            temperature=float(config.get('temperature', 0.7)),
            max_tokens=1000
        )

        reply = response.choices[0].message['content'].strip()
        return jsonify({'reply': reply})

    except Exception as e:
        return jsonify({'reply': f'שגיאה: {str(e)}'})
