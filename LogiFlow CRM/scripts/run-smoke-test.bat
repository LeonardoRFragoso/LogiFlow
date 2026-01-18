@echo off
REM =========================================
REM LogiFlow CRM - Executar Smoke Test BETA
REM =========================================

echo.
echo ========================================
echo   LogiFlow CRM - Smoke Test BETA
echo ========================================
echo.

REM Verificar se container está rodando
docker ps | findstr logiflow_api >nul 2>&1
if errorlevel 1 (
    echo ERRO: Container logiflow_api nao esta rodando
    echo Execute: setup-beta.bat primeiro
    pause
    exit /b 1
)

echo Executando testes...
echo.

docker exec logiflow_api python tests/smoke_test_beta.py

echo.
echo ========================================
echo.

if errorlevel 1 (
    echo RESULTADO: Testes FALHARAM
    echo Verifique os erros acima e corrija antes do BETA
) else (
    echo RESULTADO: Testes PASSARAM
    echo Sistema pronto para BETA!
)

echo.
pause
