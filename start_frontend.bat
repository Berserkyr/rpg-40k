@echo off
cd /d "%~dp0\frontend"
echo Lancement du frontend React sur http://localhost:5173
npm run dev -- --host=127.0.0.1 --port=5173
pause
