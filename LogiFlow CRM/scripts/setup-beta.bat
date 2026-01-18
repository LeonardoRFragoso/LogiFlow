@echo off
REM =========================================
REM LogiFlow CRM - Setup Automatizado BETA
REM =========================================
REM Script para preparar ambiente BETA em 5 minutos

echo.
echo ========================================
echo   LogiFlow CRM - Setup BETA
echo ========================================
echo.

REM Navegar para raiz do projeto
cd /d "%~dp0.."

REM 1. Verificar Docker
echo [1/6] Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker nao instalado ou nao esta rodando
    echo Instale: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo OK: Docker detectado
echo.

REM 2. Criar .env se nao existe
echo [2/6] Configurando variaveis de ambiente...
if not exist "backend\.env" (
    echo Criando backend\.env...
    copy "backend\.env.example" "backend\.env" >nul
    echo OK: backend\.env criado
) else (
    echo OK: backend\.env ja existe
)
echo.

REM 3. Iniciar containers Docker
echo [3/6] Iniciando servicos Docker (pode levar 2-3 minutos)...
docker-compose -f docker-compose.minimal.yml up -d
if errorlevel 1 (
    echo ERRO: Falha ao iniciar containers
    pause
    exit /b 1
)
echo OK: Containers iniciados
echo.

REM 4. Aguardar SuiteCRM estar pronto
echo [4/6] Aguardando SuiteCRM inicializar (30 segundos)...
timeout /t 30 /nobreak >nul
echo OK: SuiteCRM deve estar pronto
echo.

REM 5. Executar seed de dados demo
echo [5/6] Criando dados demo...
docker exec logiflow_api python scripts/seed_demo_data_simple.py
if errorlevel 1 (
    echo AVISO: Seed de dados falhou (pode ser normal se ja existe)
) else (
    echo OK: Dados demo criados
)
echo.

REM 6. Instrucoes OAuth2
echo [6/6] Configuracao OAuth2 necessaria
echo.
echo ========================================
echo   CONFIGURACAO OAUTH2 OBRIGATORIA
echo ========================================
echo.
echo 1. Acesse: http://localhost:8080
echo 2. Login: admin / admin123
echo 3. Menu: Admin -^> OAuth2 Clients
echo 4. Criar Client: LogiFlow Backend API
echo 5. Copiar CLIENT_ID e CLIENT_SECRET
echo 6. Executar: python backend\scripts\setup_oauth2_suitecrm.py
echo.
echo ========================================
echo.

REM 7. URLs de acesso
echo ACESSO AO SISTEMA:
echo   SuiteCRM:  http://localhost:8080
echo   Backend:   http://localhost:8000/api/v1/docs
echo   Frontend:  http://localhost:3001 (se rodando)
echo.

REM 8. Proximos passos
echo PROXIMOS PASSOS:
echo   1. Configurar OAuth2 (instrucoes acima)
echo   2. Executar smoke test: docker exec logiflow_api python tests/smoke_test_beta.py
echo   3. Iniciar frontend: cd frontend ^&^& npm run dev
echo.
echo ========================================
echo   Setup BETA concluido com sucesso!
echo ========================================
echo.

pause
