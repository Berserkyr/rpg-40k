@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo Lancement du backend FastAPI sur http://localhost:8000
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000 --reload
pause
