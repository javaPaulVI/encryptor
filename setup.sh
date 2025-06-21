#!/usr/bin/env bash
set -e



# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"



# Check if SCRIPT_DIR is in the permanent PATH from a fresh interactive shell
permanent_path=$(bash -ic 'echo $PATH' 2>/dev/null || echo "")

if [[ ":$permanent_path:" != *":$SCRIPT_DIR:"* ]]; then
    echo "Adding $SCRIPT_DIR to current session PATH"
    export PATH="$PATH:$SCRIPT_DIR"

    echo "Adding $SCRIPT_DIR to ~/.bashrc for future sessions"
    # Avoid duplicate entries in .bashrc
    if ! grep -Fxq "export PATH=\"\$PATH:$SCRIPT_DIR\"" ~/.bashrc; then
        echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> ~/.bashrc
    fi
fi

# Path to venv activate script
VENV_ACTIVATE="$SCRIPT_DIR/venv/bin/activate"

# Function to check if python3 venv can be created
check_venv_support() {
    python3 -m venv --help > /dev/null 2>&1 || return 1
    TMP_VENV="$SCRIPT_DIR/__temp_venv_check__"
    python3 -m venv "$TMP_VENV" > /dev/null 2>&1 || return 1
    rm -rf "$TMP_VENV"
    return 0
}

# Check for venv support and try to install python3-venv if missing on Debian/Ubuntu
if ! check_venv_support; then
    echo "Python venv module or ensurepip is missing."
    if [[ "$(uname -s)" == "Linux" ]]; then
        read -p "Try to install python3-venv package now? (requires sudo) [Y/n] " answer
        answer=${answer:-Y}
        if [[ "$answer" =~ ^[Yy]$ ]]; then
            echo "Running sudo apt update and apt install python3-venv..."
            sudo apt update && sudo apt install -y python3-venv
            echo "Please rerun the script after installation."
            exit 0
        else
            echo "Please install python3-venv manually and rerun the script."
            exit 1
        fi
    else
        echo "Automatic installation only supported on Debian/Ubuntu Linux."
        echo "Please install python3-venv manually and rerun the script."
        exit 1
    fi
fi

# Create venv if it doesn't exist
if [[ ! -f "$VENV_ACTIVATE" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "Virtual environment created at $SCRIPT_DIR/venv"
fi

# Activate the virtual environment
source "$VENV_ACTIVATE"

# Install Flask if missing
if ! pip show flask > /dev/null 2>&1; then
    echo "Installing Flask..."
    pip install flask
fi

# Install cryptography if missing
if ! pip show cryptography > /dev/null 2>&1; then
    echo "Installing cryptography..."
    pip install cryptography
fi