from flask import Flask, request, jsonify
from encryptor import Encryptor

app = Flask(__name__)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get('message', '')
    primary_key = data.get('primary_key', '')
    if not primary_key:
        return jsonify({"error": "Primary key is required"}), 400
    encryptor = Encryptor(primary_key)
    encrypted = encryptor.encrypt_message(message)
    return jsonify({"encrypted": encrypted})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    token = data.get('token', '')
    primary_key = data.get('primary_key', '')
    if not primary_key:
        return jsonify({"error": "Primary key is required"}), 400
    encryptor = Encryptor(primary_key)
    message, timestamp = encryptor.decrypt_message(token)
    return jsonify({"message": message, "timestamp": timestamp})

if __name__ == '__main__':
    app.run(debug=True, port=1555, host='localhost')