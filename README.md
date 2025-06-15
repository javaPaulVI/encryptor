# Message Encryptor

A local tool for encrypting and decrypting messages using a time-based key derivation scheme. Includes both a web interface (via Flask) and a terminal-based interface.

## Features

- **Web UI:** Encrypt and decrypt messages in your browser.
- **Terminal UI:** Command-line interface for local encryption and decryption.
- **Strong Encryption:** Uses PBKDF2, HMAC, and Fernet from the `cryptography` library.
- **Time-based Keys:** Each message is encrypted with a key derived from the current minute.
- **Primary Key Management:** Automatically generates and stores a primary key in `.primary_key` on first run.

## Requirements

- Python 3.7 or higher
- pip

## Setup

1. **Clone or Download the Repository**

   Download and extract the ZIP, or clone with:
   ```sh
   git clone https://github.com/javaPaulVI/encryptor.git
   ```

3. **Install and Run**

   Simply run: `Message-Encryptor.exe` in the current directory

   This will:
   - Set up the environment (if needed)
   - Install the libraries (if needed)
   - Start the Flask web server
   - Open the app in your browser

   > **Note:** You no longer need to manually activate a virtual environment or install dependencies separately. The program will do that if needed

4. **Primary Key Setup**

   On first run, a `.primary_key` file will be created in the project directory if it isn't already there and a random key will be generated
   - **Be cautious with sharing the key!** Anyone with access to this key can decrypt your messages.
   - You can replace the contents of `.primary_key` with your own secure, random string (URL-safe, at least 32 characters).
   - If you lose this key, you will not be able to decrypt previously encrypted messages.

## Usage

### Web Interface

The application will run on
```
http://localhost:1449
```

To run the Web interface:

- Run `Message-Encryptor.exe`
- After the Browser with the interface opens the application is ready to use

### Terminal Interface

- Run `python tui.py` to use the terminal UI.

### Issues
If you encouter any problems, feel free to register an Issue on `https://github.com/javaPaulVI/encryptor/issues`

## File Structure

- `app.py` — Flask web server
- `encryptor.py` — Encryption logic
- `tui.py` — Terminal UI
- `index.html`, `static/` — Web UI files
- `.primary_key` — Your secret encryption key (keep this safe!)

## Security

- The primary key is stored in `.primary_key` in your project directory.
- **Keep your primary key secret and secure.** Do **not** share your primary key or tokens publicly.
- Changing the key will make old messages unreadable.

## API
You will find the documentation of the API in API.md in this directory



## License

This project is licensed under the MIT License with an additional restriction for the API and Encryptor components:

You can use, modify, and redistribute the software freely for private and non-commercial purposes, including open source projects.

Commercial use of the API or encryptor — meaning use in any product or service sold, licensed, or otherwise monetized — is not allowed without explicit written permission from the author.

If you modify and redistribute the API or encryptor, you must keep the same non-commercial restriction in place for those modified versions.

For commercial licensing or permission requests, please contact: paul@be-hip.eu.