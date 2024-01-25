@echo off
cd %CD%
start "" upload_auto.bat
cd ..
call ./venv/Scripts/activate
python ./app.py
timeout /t 3