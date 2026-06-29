@echo off
echo ===================================================
echo Starting BargainAI Local Servers...
echo ===================================================

:: Start Django Backend on port 8000
echo [1/3] Launching Django backend server...
start "Django Backend Server" cmd /c "python manage.py runserver 8000 --settings=backend.settings"

:: Start Frontend Server on port 5500
echo [2/3] Launching Frontend HTTP server...
start "Frontend HTTP Server" cmd /c "cd Frontend && python -m http.server 5500"

:: Wait 3 seconds for the servers to initialize
echo [3/3] Waiting for servers to initialize...
timeout /t 3 /nobreak >nul

:: Open browser to the localhost dashboard
echo Opening browser on http://localhost:5500/dashboard.html...
start http://localhost:5500/dashboard.html

echo ===================================================
echo BargainAI is running!
echo You can close the main terminal. Keep the new windows open.
echo ===================================================
