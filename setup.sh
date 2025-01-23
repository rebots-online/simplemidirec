#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo -e "\nSetup complete! Virtual environment is active."
echo "To start recording MIDI, run: ./midi_recorder.py"
echo "When finished, type 'deactivate' to exit the virtual environment."
