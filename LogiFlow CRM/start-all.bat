@echo off
REM ============================================
REM LOGIFLOW CRM - INICIAR TODOS OS COMPONENTES
REM ============================================

echo.
echo ========================================
echo  LOGIFLOW CRM - STACK COMPLETO
echo ========================================
echo.

REM Verificar se Docker está rodando
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Docker nao esta rodando!
    echo Por favor, inicie o Docker Desktop e tente novamente.
    pause
    exit /b 1
)

echo [1/5] Parando containers antigos...
docker-compose -f docker-compose.production.yml down

echo.
echo [2/5] Limpando volumes antigos (opcional)...
REM docker volume prune -f

echo.
echo [3/5] Construindo imagens...
docker-compose -f docker-compose.production.yml build --no-cache

echo.
echo [4/5] Iniciando servicos essenciais...
docker-compose -f docker-compose.production.yml up -d db redis

echo Aguardando banco de dados inicializar...
timeout /t 15 /nobreak

echo.
echo [5/5] Iniciando todos os servicos...
docker-compose -f docker-compose.production.yml up -d

echo.
echo ========================================
echo  SERVICOS INICIADOS COM SUCESSO!
echo ========================================
echo.
echo Acessos:
echo.
echo   FRONTENDS VUE.JS:
echo   - Sistema Principal:  http://localhost:3001
echo   - App Motorista:      http://localhost:3002
echo   - Portal Cliente:     http://localhost:3003
echo   - Site Divulgacao:    http://localhost:5173
echo.
echo   BACKEND:
echo   - API FastAPI:        http://localhost:8000
echo   - SuiteCRM:           http://localhost:8080
echo.
echo   FERRAMENTAS DEV:
echo   - Adminer (DB):       http://localhost:8082
echo   - Redis Commander:    http://localhost:8081
echo.
echo Documentacao API:    http://localhost:8000/api/v1/docs
echo.
echo ========================================
echo.

REM Mostrar logs
echo Deseja ver os logs? (S/N)
set /p SHOW_LOGS=
if /i "%SHOW_LOGS%"=="S" (
    docker-compose -f docker-compose.production.yml logs -f
) else (
    echo.
    echo Para ver os logs execute:
    echo   docker-compose -f docker-compose.production.yml logs -f
    echo.
    pause
)
