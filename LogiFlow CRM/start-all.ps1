# =============================================
# LogiFlow CRM - Start All Services
# =============================================
# Execute: .\start-all.ps1
# Para parar: Ctrl+C ou feche a janela

param(
    [switch]$NoBrowser,
    [switch]$NoDocker
)

$Host.UI.RawUI.WindowTitle = "LogiFlow CRM - All Services"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   LogiFlow CRM - Iniciando Servicos   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ROOT = $PSScriptRoot

# Criar pasta de logs se não existir
$logsDir = Join-Path $ROOT "logs"
if (!(Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

# Lista de jobs para controlar
$jobs = @()

# ========== 1. Docker Services (Evolution API) ==========
if (!$NoDocker) {
    Write-Host "[1/6] Iniciando Docker (Evolution API)..." -ForegroundColor Yellow
    $evolutionPath = Join-Path $ROOT "evolution-api"
    if (Test-Path (Join-Path $evolutionPath "docker-compose.yml")) {
        $job = Start-Job -Name "Docker-Evolution" -ScriptBlock {
            param($path)
            Set-Location $path
            docker compose up 2>&1
        } -ArgumentList $evolutionPath
        $jobs += $job
        Write-Host "    Evolution API iniciando em background" -ForegroundColor Green
    } else {
        Write-Host "    Evolution API nao encontrado, pulando..." -ForegroundColor DarkGray
    }
}

Start-Sleep -Seconds 2

# ========== 2. Backend FastAPI ==========
Write-Host "[2/6] Iniciando Backend (FastAPI)..." -ForegroundColor Yellow
$backendPath = Join-Path $ROOT "backend"
$venvActivate = Join-Path $backendPath "venv\Scripts\Activate.ps1"

$job = Start-Job -Name "Backend" -ScriptBlock {
    param($path, $venv)
    Set-Location $path
    if (Test-Path $venv) {
        & $venv
    }
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 2>&1
} -ArgumentList $backendPath, $venvActivate
$jobs += $job
Write-Host "    Backend iniciando em http://localhost:8000" -ForegroundColor Green

Start-Sleep -Seconds 3

# ========== 3. Frontend Vue ==========
Write-Host "[3/6] Iniciando Frontend (Vue 3)..." -ForegroundColor Yellow
$frontendPath = Join-Path $ROOT "frontend"

$job = Start-Job -Name "Frontend" -ScriptBlock {
    param($path)
    Set-Location $path
    npm run dev 2>&1
} -ArgumentList $frontendPath
$jobs += $job
Write-Host "    Frontend iniciando em http://localhost:3000" -ForegroundColor Green

Start-Sleep -Seconds 2

# ========== 4. App Motorista ==========
Write-Host "[4/6] Iniciando App Motorista..." -ForegroundColor Yellow
$motoristaPath = Join-Path $ROOT "app-motorista"

if (Test-Path $motoristaPath) {
    $job = Start-Job -Name "AppMotorista" -ScriptBlock {
        param($path)
        Set-Location $path
        npm run dev 2>&1
    } -ArgumentList $motoristaPath
    $jobs += $job
    Write-Host "    App Motorista iniciando em http://localhost:5174" -ForegroundColor Green
}

Start-Sleep -Seconds 2

# ========== 5. Portal Cliente ==========
Write-Host "[5/6] Iniciando Portal Cliente..." -ForegroundColor Yellow
$portalPath = Join-Path $ROOT "portal-cliente"

if (Test-Path $portalPath) {
    $job = Start-Job -Name "PortalCliente" -ScriptBlock {
        param($path)
        Set-Location $path
        npm run dev 2>&1
    } -ArgumentList $portalPath
    $jobs += $job
    Write-Host "    Portal Cliente iniciando em http://localhost:5173" -ForegroundColor Green
}

Start-Sleep -Seconds 2

# ========== 6. Task Tracker ==========
Write-Host "[6/6] Iniciando Task Tracker..." -ForegroundColor Yellow
$tasksPath = Join-Path (Split-Path $ROOT -Parent) "tasks"

if (Test-Path $tasksPath) {
    $job = Start-Job -Name "TaskTracker" -ScriptBlock {
        param($path)
        Set-Location $path
        npm run dev 2>&1
    } -ArgumentList $tasksPath
    $jobs += $job
    Write-Host "    Task Tracker iniciando em http://localhost:5177" -ForegroundColor Green
}

# ========== Resumo ==========
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Todos os servicos iniciados!        " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URLs disponiveis:" -ForegroundColor White
Write-Host "  - Backend API:    http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "  - Frontend:       http://localhost:3000" -ForegroundColor Gray
Write-Host "  - App Motorista:  http://localhost:5174" -ForegroundColor Gray
Write-Host "  - Portal Cliente: http://localhost:5173" -ForegroundColor Gray
Write-Host "  - Task Tracker:   http://localhost:5177" -ForegroundColor Gray
Write-Host "  - Evolution API:  http://localhost:8080" -ForegroundColor Gray
Write-Host ""
Write-Host "Credenciais:" -ForegroundColor White
Write-Host "  - Email: admin@logiflow.com" -ForegroundColor Gray
Write-Host "  - Senha: admin123" -ForegroundColor Gray
Write-Host ""
Write-Host "Pressione Ctrl+C para parar todos os servicos" -ForegroundColor Yellow
Write-Host ""

# Abrir browser
if (!$NoBrowser) {
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000"
}

# Monitorar jobs e mostrar output
try {
    while ($true) {
        foreach ($job in $jobs) {
            $output = Receive-Job -Job $job -ErrorAction SilentlyContinue
            if ($output) {
                $color = switch ($job.Name) {
                    "Backend" { "Blue" }
                    "Frontend" { "Green" }
                    "AppMotorista" { "Magenta" }
                    "PortalCliente" { "Cyan" }
                    "TaskTracker" { "Yellow" }
                    default { "White" }
                }
                foreach ($line in $output) {
                    Write-Host "[$($job.Name)] $line" -ForegroundColor $color
                }
            }
        }
        Start-Sleep -Milliseconds 500
    }
}
finally {
    # Cleanup ao sair
    Write-Host ""
    Write-Host "Parando todos os servicos..." -ForegroundColor Red
    
    foreach ($job in $jobs) {
        Stop-Job -Job $job -ErrorAction SilentlyContinue
        Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
    }
    
    # Parar processos node que podem ter ficado
    Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Write-Host "Todos os servicos parados." -ForegroundColor Green
}
