#!/bin/bash
set -e

# Start from a clean environment
rm -rf venv/

# Basic Python3 virtual environment

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install wheel
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# If there's an error in the 'activate' step, create the environment manually
if [ ! -d "venv" ]; then
    echo "Virtual environment creation failed. Trying again..."
    python -m venv venv
    source venv/Scripts/activate  # Windows対応
    pip install --upgrade pip
    pip install wheel
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
fi
