from flask import Flask, render_template, request, jsonify
from ai_model import get_answer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json['message']
    reply = get_answer(msg)
    return jsonify({'reply': reply})

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)