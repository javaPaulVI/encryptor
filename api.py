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
    encrypted = encryptor.encrypt(message)
    return jsonify({"encrypted": encrypted})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    token = data.get('token', '')
    primary_key = data.get('primary_key', '')
    if not primary_key:
        return jsonify({"error": "Primary key is required"}), 400
    encryptor = Encryptor(primary_key)
    message, timestamp = encryptor.decrypt(token)
    return jsonify({"message": message, "timestamp": timestamp})

@app.route('/encrypt-file', methods=['POST'])
def encrypt_file():
    file = request.files.get('file')
    primary_key = request.form.get('primary_key', '')
    if not file or not primary_key:
        return jsonify({"error": "File and primary_key are required"}), 400
    message = file.read().decode("utf-8")
    encryptor = Encryptor(primary_key)
    encrypted = encryptor.encrypt(message)
    return jsonify({"encrypted": encrypted})

if __name__ == '__main__':
    app.run(debug=True, port=1555, host='localhost')