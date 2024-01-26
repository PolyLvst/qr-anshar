@echo off
cd %CD%
cd ..
if not exist "./venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing requirements...
    call ./venv/Scripts/activate
    pip install -r "./requirements.txt"
) else (
    call ./venv/Scripts/activate
)
if not exist ".env" (
    echo No .env file found, please check again
    timeout /t 3
    exit
)
start "" ./windows/upload_auto.bat
echo IP Address : 
ipconfig | findstr /i "IPv4"
echo Port : 5000
waitress-serve --listen=0.0.0.0:5000 app:app
timeout /t 3