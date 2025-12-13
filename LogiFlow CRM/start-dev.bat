@echo off
title LogiFlow CRM - Dev Environment
color 0A

echo.
echo ========================================
echo   LogiFlow CRM - Ambiente de Dev
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Iniciando Backend...
start "Backend" cmd /k "cd backend && IF EXIST venv\Scripts\activate.bat (call venv\Scripts\activate.bat) && python -m uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2/5] Iniciando Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 2 /nobreak >nul

echo [3/5] Iniciando App Motorista...
start "App Motorista" cmd /k "cd app-motorista && npm run dev"

timeout /t 2 /nobreak >nul

echo [4/5] Iniciando Portal Cliente...
start "Portal Cliente" cmd /k "cd portal-cliente && npm run dev"

timeout /t 2 /nobreak >nul

echo [5/5] Iniciando Task Tracker...
start "Task Tracker" cmd /k "cd ..\tasks && npm run dev"

echo.
echo ========================================
echo   Todos os servicos iniciados!
echo ========================================
echo.
echo URLs:
echo   Backend:        http://localhost:8000/docs
echo   Frontend:       http://localhost:3000
echo   App Motorista:  http://localhost:5175
echo   Portal Cliente: http://localhost:5173
echo   Task Tracker:   http://localhost:5177
echo.
echo Login: admin@logiflow.com / admin123
echo.
echo Pressione qualquer tecla para abrir o navegador...
pause >nul

start http://localhost:3000
