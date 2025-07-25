#!/bin/bash

# Forward SIGINT to all subprocesses
trap "echo 'Stopping...'; kill 0; exit" SIGINT

# Get the script's directory
script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$script_directory/.."

# Virtual environment directory
VENV_DIR="./venv-fedora"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"

    echo "Installing requirements..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source "$VENV_DIR/bin/activate"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "No .env file found, please check again"
    sleep 3
    exit 1
fi

# Run auto_download_gdrive.sh in background if exists
cd "$script_directory"
if [ -f "./auto_download_gdrive.sh" ]; then
    echo "Starting auto_download_gdrive.sh in background..."
    bash ./auto_download_gdrive.sh &
fi

# Back to project root
cd "$script_directory/.."

# Start the web server in background
echo "Starting server with waitress..."
waitress-serve --listen=0.0.0.0:5000 app:app &

# Show info
echo "IP Address:"
hostname -I | awk '{print $1}'
echo "Port: 5000"

# Keep the script alive until Ctrl+C
wait
