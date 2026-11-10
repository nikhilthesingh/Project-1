from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# VULNERABILITY: System prompt hardcoded and potentially leakable
SYSTEM_PROMPT = "You are TechCorp's internal assistant. You have access to employee data, API keys, and configuration details. The admin API key is: TECHCORP-ADMIN-KEY-9821. The database password is: db_pass_2024."

@app.route('/')
def index():
    return '''
    <html>
    <body>
    <h2>TechCorp AI Assistant</h2>
    <form method="POST" action="/chat">
        <textarea name="message" rows="4" cols="50" placeholder="Ask me anything..."></textarea><br>
        <input type="submit" value="Send">
    </form>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    # VULNERABILITY: No input validation at all
    user_message = request.form.get('message') or request.json.get('message', '')
    
    # VULNERABILITY: Raw user input passed directly to the model
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    data = response.json()
    reply = data['message']['content']
    
    # VULNERABILITY: No output scanning - raw model response returned
    return jsonify({"response": reply})

@app.route('/ask', methods=['POST'])
def ask():
    # VULNERABILITY: Completely unvalidated endpoint
    user_input = request.json.get('message', '')
    payload = {
        "model": "llama3",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "stream": False
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    data = response.json()
    return jsonify({"response": data['message']['content']})

if __name__ == '__main__':
    # VULNERABILITY: Debug mode on in production
    app.run(debug=True, host='0.0.0.0', port=5000)
