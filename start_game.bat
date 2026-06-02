@echo off
cd /d "%~dp0"
echo Nettoyage des ports 8000 et 5173...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ports=@(8000,5173); foreach($p in $ports){ $ids=(Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique); foreach($id in $ids){ if($id -and $id -ne $PID){ Stop-Process -Id $id -Force -ErrorAction SilentlyContinue } } }"
echo Lancement du backend...
start "Survivant Backend" "%~dp0start_backend.bat"
echo Lancement du frontend...
start "Survivant Frontend" "%~dp0start_frontend.bat"
timeout /t 4 /nobreak >nul
start http://localhost:5173
echo Jeu lance sur http://localhost:5173
pause
