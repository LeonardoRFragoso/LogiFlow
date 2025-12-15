# =============================================
# LogiFlow CRM - Deploy Automático
# PowerShell Script
# =============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LogiFlow CRM - Deploy para GitHub   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Diretório do projeto
$PROJECT_DIR = "C:\Users\leonardo.fragoso\OneDrive - INTERNATIONAL CONTAINER TERMINAL SERVICES\Área de Trabalho\Projetos\SuiteCRM"

# Ir para o diretório
Set-Location $PROJECT_DIR

# 1. Status do Git
Write-Host "[STATUS] Verificando status do Git..." -ForegroundColor Blue
git status
Write-Host ""

# 2. Verificar se é repositório Git
if (-not (Test-Path ".git")) {
    Write-Host "[INIT] Inicializando repositório Git..." -ForegroundColor Yellow
    git init
    Write-Host "OK - Repositório inicializado!" -ForegroundColor Green
    Write-Host ""
}

# 3. Configurar Git (se necessário)
$gitName = git config user.name
if ([string]::IsNullOrEmpty($gitName)) {
    Write-Host "[CONFIG] Configurando Git..." -ForegroundColor Yellow
    git config user.name "Leonardo Fragoso"
    git config user.email "leonardo.fragoso@ictsi.com"
    Write-Host "OK - Git configurado!" -ForegroundColor Green
    Write-Host ""
}

# 4. Adicionar todos os arquivos
Write-Host "[ADD] Adicionando arquivos ao Git..." -ForegroundColor Blue
git add .
Write-Host "OK - Arquivos adicionados!" -ForegroundColor Green
Write-Host ""

# 5. Criar commit
Write-Host "[COMMIT] Criando commit..." -ForegroundColor Blue
$COMMIT_MSG = Read-Host "Digite a mensagem do commit (ou Enter para padrão)"

if ([string]::IsNullOrEmpty($COMMIT_MSG)) {
    $COMMIT_MSG = @"
Deploy: LogiFlow CRM v1.0.0 - 100% Concluído

Features Implementadas:
- Backend FastAPI completo (30+ routers)
- Frontend Vue 3 responsivo  
- GPS Tracking tempo real
- Cotação Automática multi-fontes
- NPS/CSAT automático
- Multi-tenancy completo
- Integrações self-service
- PWAs (Motorista + Cliente)
- 11 documentações completas
- Configuração Render.com

201/201 Tasks Concluídas
Pronto para produção!
"@
}

git commit -m $COMMIT_MSG

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK - Commit criado!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Aviso: Nada para commitar ou commit já existe" -ForegroundColor Yellow
    Write-Host ""
}

# 6. Verificar remote
Write-Host "[REMOTE] Verificando remote origin..." -ForegroundColor Blue
$remote = git remote get-url origin 2>$null

if ([string]::IsNullOrEmpty($remote)) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  CONFIGURAR REPOSITÓRIO GITHUB" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Acesse: https://github.com/new" -ForegroundColor White
    Write-Host "2. Nome: logiflow-crm" -ForegroundColor White
    Write-Host "3. Privado: SIM" -ForegroundColor White
    Write-Host "4. NÃO adicione README ou .gitignore" -ForegroundColor White
    Write-Host "5. Clique em 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    $GIT_URL = Read-Host "Cole a URL do repositório (https://github.com/SEU_USUARIO/logiflow-crm.git)"
    
    if (-not [string]::IsNullOrEmpty($GIT_URL)) {
        git remote add origin $GIT_URL
        Write-Host "OK - Remote adicionado!" -ForegroundColor Green
        $remote = $GIT_URL
    }
} else {
    Write-Host "OK - Remote já configurado: $remote" -ForegroundColor Green
}
Write-Host ""

# 7. Push para GitHub
if (-not [string]::IsNullOrEmpty($remote)) {
    Write-Host "[PUSH] Enviando para GitHub..." -ForegroundColor Blue
    Write-Host ""
    
    # Verificar se branch main existe
    $currentBranch = git branch --show-current
    if ($currentBranch -ne "main") {
        Write-Host "Renomeando branch para 'main'..." -ForegroundColor Yellow
        git branch -M main
    }
    
    # Push
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "  CÓDIGO ENVIADO COM SUCESSO!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "PRÓXIMOS PASSOS:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Acesse: https://dashboard.render.com" -ForegroundColor White
        Write-Host "2. Clique em: New + → Blueprint" -ForegroundColor White
        Write-Host "3. Conecte seu repositório GitHub" -ForegroundColor White
        Write-Host "4. Selecione: logiflow-crm" -ForegroundColor White
        Write-Host "5. Branch: main" -ForegroundColor White
        Write-Host "6. Render detectará o render.yaml" -ForegroundColor White
        Write-Host "7. Configure variáveis de ambiente" -ForegroundColor White
        Write-Host "8. Clique em Apply" -ForegroundColor White
        Write-Host ""
        Write-Host "Documentação: GUIA_COMMIT_GITHUB.md" -ForegroundColor Yellow
        Write-Host "Deploy Guide: LogiFlow CRM\DEPLOY_RENDER.md" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "URLs após deploy:" -ForegroundColor Cyan
        Write-Host "  Frontend: https://logiflow-frontend.onrender.com" -ForegroundColor White
        Write-Host "  Backend:  https://logiflow-api.onrender.com" -ForegroundColor White
        Write-Host "  Docs:     https://logiflow-api.onrender.com/docs" -ForegroundColor White
        Write-Host ""
        Write-Host "Deploy automático iniciará!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "  ERRO NO PUSH" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host ""
        Write-Host "Possíveis causas:" -ForegroundColor Yellow
        Write-Host "  1. Credenciais GitHub não configuradas" -ForegroundColor White
        Write-Host "  2. Repositório não existe" -ForegroundColor White
        Write-Host "  3. Sem permissão de push" -ForegroundColor White
        Write-Host ""
        Write-Host "Soluções:" -ForegroundColor Yellow
        Write-Host "  - Configure credenciais: git config --global credential.helper wincred" -ForegroundColor White
        Write-Host "  - Use HTTPS em vez de SSH" -ForegroundColor White
        Write-Host "  - Verifique se o repositório existe no GitHub" -ForegroundColor White
        Write-Host ""
        Write-Host "Consulte: GUIA_COMMIT_GITHUB.md para mais ajuda" -ForegroundColor Cyan
        Write-Host ""
    }
}

Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

