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

3. **Set your primary key**  
   On first run, a file named `.primary_key` will be created in the project directory containing your encryption key.  
   - **Keep this key secret!** Anyone with access to this key can decrypt your messages.
   - You can customize your key by editing the `.primary_key` file and replacing its contents with your own secure, random string (URL-safe, at least 32 characters).
   - If you lose this key, you will not be able to decrypt previously encrypted messages.

4. **Run the app**  
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
- [`.primary_key`](.primary_key ) — Your secret encryption key (keep this safe!)

## Security

- The primary key is stored in the `.primary_key` file in your project directory.
- **Keep your primary key secret and secure.** Do **not** share your primary key or tokens publicly.
- You can change your key at any time by editing the `.primary_key` file, but old messages encrypted with the previous key will become unreadable.

## License

MIT License (see LICENCE file)