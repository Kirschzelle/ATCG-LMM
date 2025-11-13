@echo off
echo Installing with ROCm support for AMD GPUs...
python -m venv env
call env\Scripts\activate.bat
set CMAKE_ARGS=-DGGML_HIPBLAS=on
pip install llama-cpp-python --force-reinstall --no-cache-dir
pip install -r requirements.txt
echo.
echo Installation complete! Starting application...
python ./src/main.py
pause