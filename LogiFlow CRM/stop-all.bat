@echo off
title LogiFlow CRM - Stop All
color 0C

echo.
echo ========================================
echo   LogiFlow CRM - Parando Servicos
echo ========================================
echo.

echo Parando processos Node.js...
taskkill /F /IM node.exe 2>nul

echo Parando processos Python...
taskkill /F /IM python.exe 2>nul

echo.
echo ========================================
echo   Todos os servicos parados!
echo ========================================
echo.
pause
