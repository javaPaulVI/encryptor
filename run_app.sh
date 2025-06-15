#!/usr/bin/env bash
set -e


chmod +x "$SCRIPT_DIR/setup.sh"



# Open default browser to http://localhost:1556
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:1556
elif command -v open > /dev/null; then
    open http://localhost:1556
else
    echo "Please open http://localhost:1556 manually"
fi

# Run the Flask app in a new terminal (detached)
if command -v gnome-terminal > /dev/null; then
    gnome-terminal -- bash -c "cd '$SCRIPT_DIR'; source venv/bin/activate; python app.py; exec bash"
elif command -v x-terminal-emulator > /dev/null; then
    x-terminal-emulator -e bash -c "cd '$SCRIPT_DIR'; source venv/bin/activate; python app.py"
else
    echo "Launching Flask app in the current terminal..."
    python app.py
fi
