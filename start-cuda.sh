#!/bin/bash
echo "Installing with CUDA support for NVIDIA GPUs..."
python3 -m venv env
source env/bin/activate
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install -r requirements.txt
echo ""
echo "Installation complete! Starting application..."
python ./src/main.py