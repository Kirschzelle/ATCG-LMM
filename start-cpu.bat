@echo off
echo Installing for CPU only...
python -m venv env
call env\Scripts\activate.bat
pip install llama-cpp-python
pip install -r requirements.txt
echo.
echo Installation complete! Starting application...
python ./src/main.py
pause