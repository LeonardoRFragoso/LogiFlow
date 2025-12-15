@echo off
REM =============================================
REM LogiFlow CRM - Commit e Preparar Deploy (Windows)
REM =============================================

echo.
echo ========================================
echo   LogiFlow CRM - Deploy para Render
echo ========================================
echo.

REM 1. Status do Git
echo [STATUS] Verificando status do Git...
git status
echo.

REM 2. Adicionar todos os arquivos
echo [ADD] Adicionando arquivos ao Git...
git add .
echo OK - Arquivos adicionados!
echo.

REM 3. Commit
echo [COMMIT] Criando commit...
set /p COMMIT_MSG="Digite a mensagem do commit (ou Enter para padrao): "

if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Deploy: LogiFlow CRM 100%% Concluido - Ready for Production
)

git commit -m "%COMMIT_MSG%"
echo OK - Commit criado!
echo.

REM 4. Push para GitHub
echo [PUSH] Enviando para GitHub...
set /p BRANCH="Branch para push (padrao: main): "

if "%BRANCH%"=="" (
    set BRANCH=main
)

git push origin %BRANCH%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   CODIGO ATUALIZADO NO GITHUB!
    echo ========================================
    echo.
    echo PROXIMOS PASSOS:
    echo.
    echo 1. Acesse: https://dashboard.render.com
    echo 2. Clique em: New + -^> Blueprint
    echo 3. Conecte seu repositorio GitHub
    echo 4. Selecione a branch: %BRANCH%
    echo 5. O Render detectara automaticamente o render.yaml
    echo 6. Configure as variaveis de ambiente
    echo 7. Clique em Apply
    echo.
    echo Documentacao: LogiFlow CRM\DEPLOY_RENDER.md
    echo.
    echo URLs apos deploy:
    echo   Frontend: https://logiflow-frontend.onrender.com
    echo   Backend:  https://logiflow-api.onrender.com
    echo   Docs:     https://logiflow-api.onrender.com/docs
    echo.
    echo Deploy automatico iniciara apos conectar no Render!
    echo.
) else (
    echo.
    echo [ERRO] Falha no push. Verifique:
    echo   1. Remote origin configurado?
    echo      git remote add origin ^<URL_DO_SEU_REPOSITORIO^>
    echo   2. Credenciais do GitHub configuradas?
    echo   3. Branch existe no remoto?
    echo.
)

pause

