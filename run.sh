#!/bin/bash


# Exit on error
set -e

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate the virtual environment
source venv/bin/activate
echo "Virtual environment activated."

# Install dependencies
pip install -r requirements.txt
echo "Dependencies installed."

# Create the instance directory if it doesn't exist
mkdir -p instance
