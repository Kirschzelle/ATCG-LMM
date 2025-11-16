#!/bin/bash
echo "Installing with Metal support for Apple Silicon..."
python3 -m venv env
source env/bin/activate
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --no-cache-dir
pip install -r requirements.txt
echo ""
echo "Installation complete! Starting application..."
python ./src/main.py