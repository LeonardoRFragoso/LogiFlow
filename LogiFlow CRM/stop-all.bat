@echo off
REM ============================================
REM LOGIFLOW CRM - PARAR TODOS OS COMPONENTES
REM ============================================

echo.
echo ========================================
echo  LOGIFLOW CRM - PARANDO SERVICOS
echo ========================================
echo.

echo [1/3] Parando containers Docker...
docker-compose -f docker-compose.production.yml down

echo.
echo [2/3] Parando processos Node.js locais...
taskkill /F /IM node.exe 2>nul

echo.
echo [3/3] Parando processos Python locais...
taskkill /F /IM python.exe 2>nul

echo.
echo ========================================
echo  TODOS OS SERVICOS PARADOS!
echo ========================================
echo.
echo Para remover volumes (CUIDADO - apaga dados):
echo   docker-compose -f docker-compose.production.yml down -v
echo.
pause
