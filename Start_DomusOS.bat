@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (set PY=py) else (set PY=python)
%PY% -m pip install -r requirements.txt
if errorlevel 1 (echo Could not install requirements. Check your internet connection and Python installation. pause & exit /b 1)
start "DomusOS" http://127.0.0.1:8767
%PY% app.py
pause
