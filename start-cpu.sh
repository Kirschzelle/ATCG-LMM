#!/bin/bash
echo "Installing for CPU only..."
python3 -m venv env
source env/bin/activate
pip install llama-cpp-python --no-cache-dir
pip install -r requirements.txt
echo ""
echo "Installation complete! Starting application..."
python ./src/main.py