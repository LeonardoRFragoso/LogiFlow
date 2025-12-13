$ErrorActionPreference = "Stop"

$VERSION = "8.6.1"
$URL = "https://github.com/salesagility/SuiteCRM-Core/releases/download/v$VERSION/SuiteCRM-$VERSION.zip"
$DEST = ".\suitecrm"

Write-Host "Instalando SuiteCRM $VERSION..." -ForegroundColor Cyan

$TEMP = Join-Path $env:TEMP "suitecrm_$(Get-Date -Format 'yyyyMMddHHmmss')"
New-Item -ItemType Directory -Path $TEMP -Force | Out-Null

Write-Host "Baixando..." -ForegroundColor Green
$zip = Join-Path $TEMP "suitecrm.zip"
Invoke-WebRequest -Uri $URL -OutFile $zip -UseBasicParsing

Write-Host "Extraindo..." -ForegroundColor Green
Expand-Archive -Path $zip -DestinationPath $TEMP -Force

Write-Host "Instalando..." -ForegroundColor Green
if (!(Test-Path $DEST)) {
    New-Item -ItemType Directory -Path $DEST -Force | Out-Null
}

$extracted = Get-ChildItem -Path $TEMP -Directory | Where-Object { $_.Name -like "SuiteCRM-*" } | Select-Object -First 1
Get-ChildItem -Path $extracted.FullName -Force | ForEach-Object {
    $d = Join-Path $DEST $_.Name
    if (Test-Path $d) { Remove-Item -Path $d -Recurse -Force }
    Move-Item -Path $_.FullName -Destination $DEST -Force
}

Write-Host "Criando configuracao..." -ForegroundColor Green
$env = "APP_ENV=prod`nAPP_SECRET=change-this`nDATABASE_URL=`"mysql://logiflow:logiflow123@db:3306/logiflow_crm?serverVersion=10.6`"`nSITE_URL=http://localhost:8080"
Set-Content -Path "$DEST\.env.local" -Value $env -Encoding UTF8

Remove-Item -Path $TEMP -Recurse -Force

Write-Host "`nConcluido!" -ForegroundColor Green
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "1. docker-compose up -d"
Write-Host "2. Acesse http://localhost:8080/install.php"
Write-Host ""
