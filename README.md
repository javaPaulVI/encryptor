# Message Encryptor

A simple web and terminal-based tool for encrypting and decrypting messages using a time-based key derivation scheme.

## Features

- **Web UI**: Encrypt and decrypt messages in your browser.
- **Terminal UI**: Command-line interface for local encryption/decryption.
- **Strong Encryption**: Uses PBKDF2, HMAC, and Fernet from the `cryptography` library.
- **Time-based Keys**: Each message is encrypted with a key derived from the current minute.

## Requirements

- Python 3.7+
- pip

## Setup

1. **Clone the repository**  
   (or download and extract the ZIP)

2. **Install dependencies and set up environment**  
   On Windows, run:
   ```bat
   setup_project.bat
   ```
   This will:
   - Create a virtual environment
   - Install required libraries
   - Set the `PRIMARY_KEY` environment variable

3. **Run the app**  
   ```bat
   run_app.bat
   ```
   This will:
   - Activate the virtual environment
   - Start the Flask web server
   - Open the app in your browser

## Usage

### Web Interface

- Open [http://127.0.0.1:5000](http://127.0.0.1:5000)
- Enter a message to encrypt or a token to decrypt.

### Terminal Interface

Run:
```sh
python tui.py
```
Follow the prompts to encrypt or decrypt messages.

## File Structure

- [`app.py`](app.py ) — Flask web server
- [`encryptor.py`](encryptor.py ) — Encryption logic
- [`tui.py`](tui.py ) — Terminal UI
- [`index.html`](index.html ), [`static`](static ) — Web UI files
- [`commands/windows`](commands/windows ) — Windows setup scripts

## Security

- The primary key is stored as an environment variable (`PRIMARY_KEY`).
- Do **not** share your primary key or tokens publicly.

## License

Find the license in the LICENCE file in this direcory