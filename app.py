import random
from flask import Flask, request, jsonify, send_from_directory
from encryptor import Encryptor
import secrets
import os



def get_primary_key():
    KEY_FILE = ".primary_key"
    key = None
    if os.path.isfile(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = f.read().strip()
    else:
        print(f"Primary key file {KEY_FILE} not found. Creating {KEY_FILE} and generating a new key.")
        key = secrets.token_urlsafe(32)
        with open(KEY_FILE, "w") as f:
            f.write(key)

    if not key:
        key = secrets.token_urlsafe(32)
        print(f"Generated primary key: {key}")
        print(f"Saved primary key to {KEY_FILE}")
        print("For a custom primary key, change the content of the .primary_key file.")
        with open(KEY_FILE, "w") as f:
            f.write(key)
    return key

app = Flask(__name__)
primary_key = get_primary_key()
encryptor = Encryptor(primary_key)




@app.route('/')
def index():

    return send_from_directory('.', 'index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    file_content = False
    data = request.json
    message = data.get('message', '')
    try:
        if os.path.isfile(message):
            with open(message, 'r') as file:
                file_content = True
                message = file.readlines()
                message = ''.join(message).strip()
        encrypted = encryptor.encrypt(message)
        return jsonify({"encrypted": encrypted+str(random.randint(0, 4)) if file_content else encrypted+str(random.randint(5, 9))})
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file_content = False
    data = request.json
    token = data.get('token', '')
    if int(token[-1]) in range(0,5):
        file_content = True
    elif int(token[-1]) in range(5,10):
        file_content = False
    token = token[:-1]

    try:
        message, timestamp = encryptor.decrypt(token)
        return jsonify({"message": "Message: "+message, "timestamp": timestamp} if not file_content else {"message": "Message from File:\n\n"+message, "timestamp": timestamp})
    except Exception as e:
        return jsonify({"Error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=1556, host='localhost')
