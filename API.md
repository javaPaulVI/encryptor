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

## Example Usage

### Python Example

You can make requests to the API  using the module `requests`
````python
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

````

### JavaScript Example (Browser Console)

You can make requests to the API directly from your browser's developer console using `fetch`:

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