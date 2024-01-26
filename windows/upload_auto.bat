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
echo Script ini untuk mengupload absen hari ini ke erina
:loop
python ./lazy_attend.py
ping 127.0.0.1 -n 4 > nul
goto loop