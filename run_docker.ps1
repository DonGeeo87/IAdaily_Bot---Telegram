# Script para ejecutar el bot con Docker
# run_docker.ps1

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  IA Daily Bot - Docker Runner" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Ruta de Docker
$docker = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
$dockerCompose = "C:\Program Files\Docker\Docker\resources\bin\docker-compose.exe"

# Cambiar al directorio del proyecto
Set-Location $PSScriptRoot

Write-Host "[1/4] Verificando Docker..." -ForegroundColor Yellow
& $docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker no esta instalado o no esta corriendo" -ForegroundColor Red
    exit 1
}
Write-Host "OK" -ForegroundColor Green
Write-Host ""

Write-Host "[2/4] Construyendo imagen..." -ForegroundColor Yellow
& $docker build -t iadaily-bot .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Fallo la construccion de la imagen" -ForegroundColor Red
    exit 1
}
Write-Host "OK" -ForegroundColor Green
Write-Host ""

Write-Host "[3/4] Iniciando contenedor..." -ForegroundColor Yellow
& $docker run -d `
    --name iadaily-bot `
    --restart unless-stopped `
    -e TELEGRAM_BOT_TOKEN="8627686733:AAGgyqXtPu1juP1hjGZbb0iIhJWhq2WN324" `
    -e TELEGRAM_CHANNEL_ID="@IADailyChannel" `
    -e TELEGRAM_ADMIN_USERS="2036304183" `
    -e TIMEZONE="America/Mexico_City" `
    -v "${PWD}\logs:/app/logs" `
    -v "${PWD}\posts:/app/posts" `
    iadaily-bot

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Fallo al iniciar el contenedor" -ForegroundColor Red
    exit 1
}
Write-Host "OK" -ForegroundColor Green
Write-Host ""

Write-Host "[4/4] Verificando estado..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
& $docker ps --filter "name=iadaily-bot"
Write-Host ""

Write-Host "====================================" -ForegroundColor Green
Write-Host "  BOT INICIADO EXITOSAMENTE!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos utiles:" -ForegroundColor Cyan
Write-Host "  Ver logs:     docker logs -f iadaily-bot" -ForegroundColor White
Write-Host "  Detener:      docker stop iadaily-bot" -ForegroundColor White
Write-Host "  Reiniciar:    docker restart iadaily-bot" -ForegroundColor White
Write-Host "  Eliminar:     docker rm -f iadaily-bot" -ForegroundColor White
Write-Host ""
