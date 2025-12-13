$ErrorActionPreference = "Stop"

Write-Host "Instalando SuiteCRM via caminho curto..." -ForegroundColor Cyan

# 1. Criar pasta temporaria em C:\
Write-Host "Criando pasta temporaria..." -ForegroundColor Green
New-Item -ItemType Directory -Path "C:\Temp\SuiteCRM" -Force | Out-Null

# 2. Baixar SuiteCRM
Write-Host "Baixando SuiteCRM 8.6.1..." -ForegroundColor Green
$url = "https://github.com/salesagility/SuiteCRM-Core/releases/download/v8.6.1/SuiteCRM-8.6.1.zip"
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri $url -OutFile "C:\Temp\SuiteCRM.zip" -UseBasicParsing
$ProgressPreference = 'Continue'
Write-Host "Download concluido!" -ForegroundColor Green

# 3. Extrair em C:\Temp (caminho curto!)
Write-Host "Extraindo arquivos..." -ForegroundColor Green
Expand-Archive -Path "C:\Temp\SuiteCRM.zip" -DestinationPath "C:\Temp\SuiteCRM" -Force
Write-Host "Extracao concluida!" -ForegroundColor Green

# 4. Copiar para o projeto
Write-Host "Copiando para o projeto..." -ForegroundColor Green
$origem = "C:\Temp\SuiteCRM\SuiteCRM-8.6.1"
$destino = ".\suitecrm"

if (!(Test-Path $destino)) {
    New-Item -ItemType Directory -Path $destino -Force | Out-Null
}

Get-ChildItem -Path $origem -Force | ForEach-Object {
    $dest = Join-Path $destino $_.Name
    if (Test-Path $dest) {
        Remove-Item -Path $dest -Recurse -Force
    }
    Copy-Item -Path $_.FullName -Destination $destino -Recurse -Force
}
Write-Host "Copia concluida!" -ForegroundColor Green

# 5. Criar arquivo .env.local
Write-Host "Criando configuracao..." -ForegroundColor Green
$envContent = @"
APP_ENV=prod
APP_SECRET=change-this-to-random-string
DATABASE_URL="mysql://logiflow:logiflow123@db:3306/logiflow_crm?serverVersion=10.6"
SITE_URL=http://localhost:8080
LEGACY_SESSION_NAME=LEGACYSESSID
"@
Set-Content -Path "$destino\.env.local" -Value $envContent -Encoding UTF8
Write-Host "Configuracao criada!" -ForegroundColor Green

# 6. Limpar arquivos temporarios
Write-Host "Limpando arquivos temporarios..." -ForegroundColor Green
Remove-Item "C:\Temp\SuiteCRM" -Recurse -Force
Remove-Item "C:\Temp\SuiteCRM.zip" -Force
Write-Host "Limpeza concluida!" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "SuiteCRM instalado com sucesso!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Yellow
Write-Host "1. Execute: docker-compose up -d"
Write-Host "2. Acesse: http://localhost:8080/install.php"
Write-Host "3. Complete a instalacao via interface web"
Write-Host ""
