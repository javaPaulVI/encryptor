# Message Encryptor API Documentation

This API allows you to encrypt and decrypt messages using a time-based key derivation scheme. It is intended for local use only. With modification it can be transformed to a server-based API.

## Base URL

```
http://localhost:1555
```

---

## Usage

Before querying the API, run api.py first then use the Base URL for POST requests

## Endpoints

### POST `/encrypt`

Encrypt a message with a provided primary key.

- **Request Body (JSON):**
  ```json
  {
    "message": "Your message here",
    "primary_key": "your_primary_key_here"
  }
  ```

- **Response (JSON):**
  ```json
  {
    "encrypted": "ENCRYPTED_TOKEN"
  }
  ```

---

### POST `/decrypt`

Decrypt a token with a provided primary key.

- **Request Body (JSON):**
  ```json
  {
    "token": "ENCRYPTED_TOKEN",
    "primary_key": "your_primary_key_here"
  }
  ```

- **Response (JSON):**
  ```json
  {
    "message": "Decrypted message",
    "timestamp": "Timestamp info"
  }
  ```

---

### POST `/encrypt-file`

Encrypt the contents of a file.

- **Request:** `multipart/form-data` with fields:
  - `file`: The file to encrypt
  - `primary_key`: Your primary key

- **Response:**
  ```json
  {
    "encrypted": "ENCRYPTED_TOKEN"
  }
  ```

---

## API Usage

### Requests via http


#### Python Example

```python
import requests

# Encrypt a message
encrypt_resp = requests.post(
    "http://localhost:1555/encrypt",
    json={"message": "Hello, world!", "primary_key": "your_primary_key_here"}
)
print(encrypt_resp.json())

# Decrypt a message
decrypt_resp = requests.post(
    "http://localhost:1555/decrypt",
    json={"token": "ENCRYPTED_TOKEN", "primary_key": "your_primary_key_here"}
)
print(decrypt_resp.json())

```

#### JavaScript Example (Browser Console)

```javascript
// Encrypt a message
fetch('http://localhost:1555/encrypt', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Hello, world!',
    primary_key: 'your_primary_key_here'
  })
})
  .then(response => response.json())
  .then(data => console.log('Encrypted:', data));

// Decrypt a message
fetch('http://localhost:1555/decrypt', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    token: 'ENCRYPTED_TOKEN',
    primary_key: 'your_primary_key_here'
  })
})
  .then(response => response.json())
  .then(data => console.log('Decrypted:', data));

  
```

---

###  Usage of the python class `Encyptor`

```Python
from encryptor import Encryptor

encryptor = Encryptor("your_primary_key")


# Encrypt a message
encrypted_message = encryptor.encrypt("your_message")

print(encrypted_message)

# Decrypt a message
decrypted_message = encryptor.decrypt("encrypted_token")
print(decrypted_message)

#Encrypt a file
with open("path") as f:
  content = f.readlines()

encrypted_message_from_file = encryptor.encrypt(content)
print(encrypted_message_from_file)

```
---

## Notes

- This API is not created for a Server; do not expose it to the internet without proper security.
- The `primary_key` must be provided with each request and should be kept secret.
