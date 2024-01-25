@echo off
cd %CD%
cd ..
call ./venv/Scripts/activate
:loop
python ./lazy_attend.py
timeout /t 10
goto loop