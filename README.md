# Message Encryptor

A local tool for encrypting and decrypting messages using a time-based key derivation scheme. Includes both a web interface (via Flask) and a terminal-based interface.

## Features

- **Web UI:** Encrypt and decrypt messages in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).
- **Terminal UI:** Command-line interface for local encryption and decryption.
- **Strong Encryption:** Uses PBKDF2, HMAC, and Fernet from the `cryptography` library.
- **Time-based Keys:** Each message is encrypted with a key derived from the current minute.
- **Primary Key Management:** The API now expects the primary key to be provided with each request.
- **File Encryption:** Encrypt files via TUI or the web interface.

## Requirements

- Python 3.7 or higher
- pip

## Setup

### Windows

Run:
```bat
run_app.bat
```

### Linux

Run the setup script:
   ```sh
   chmod +x run_app.sh
   ./run_app.sh
   ```


## Web Application

After running the app, open [http://localhost:1555](http://localhost:1555) in your browser.  
You can use the web interface to:
- Enter a message and your primary key to encrypt a message.
- Paste an encrypted token and your primary key to decrypt a message.
## TUI (Terminal UI)

- You can now specify a file path to encrypt its contents.
- If no file path is given, you can type your message directly.

## API

See [API.md](API.md) for full API documentation, including file upload support.

## License

MIT License (see LICENSE file)

---

This software may be used in open source projects, including those that do not charge money to users, and may be integrated into local or private APIs, provided that all other terms of this license are followed.