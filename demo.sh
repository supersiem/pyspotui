#!/bin/bash

echo "Making Python virtual environment for the demo..."
python3 -m venv demo_venv
source demo_venv/bin/activate
pip install rich spotipy requests
echo "Creating SECRETS.py from _SECRETS.py template..."
if [ -f "_SECRETS.py" ]; then
    cp _SECRETS.py SECRETS.py
    echo "SECRETS.py created. Please fill in your Spotify API credentials."
    nano SECRETS.py
else
    echo "Error: _SECRETS.py template not found."
    exit 1
fi
python main.py