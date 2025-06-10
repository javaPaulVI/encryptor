from flask import Flask, request, jsonify, send_from_directory
from encryptor import Encryptor  # Import your Encryptor class
import os

app = Flask(__name__)

primary_key = os.environ.get('PRIMARY_KEY', 'yourFallbackPrimaryKey')
encryptor = Encryptor(primary_key)

@app.route('/')
def index():
    # Serve index.html from the same directory as this app.py file
    return send_from_directory('.', 'index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get('message', '')
    try:
        encrypted = encryptor.encrypt_message(message)
        return jsonify({"encrypted": encrypted})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    token = data.get('token', '')
    try:
        message, timestamp = encryptor.decrypt_message(token)
        return jsonify({"message": message, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
