@echo off
REM 🚀 Deploy a fly.io - Script para Windows
REM Uso: deploy_fly.bat

echo ╔═══════════════════════════════════════════════╗
echo    🚀 IA Daily Bot - Deploy a fly.io
echo ╚═══════════════════════════════════════════════╝
echo.

REM Verificar flyctl
echo [1/5] Verificando flyctl...
where fly >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ flyctl no encontrado
    echo.
    echo 📦 Instalar flyctl:
    echo    winget install fly.flyctl
    echo.
    pause
    exit /b 1
)
echo ✅ flyctl encontrado
fly version
echo.

REM Verificar autenticación
echo [2/5] Verificando autenticacion...
fly auth whoami >nul 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  No has iniciado sesion en fly.io
    echo.
    echo Iniciando sesion...
    fly auth login
    if %errorlevel% neq 0 (
        echo ❌ Error al iniciar sesion
        pause
        exit /b 1
    )
)
echo ✅ Sesion activa
echo.

REM Verificar archivos
echo [3/5] Verificando archivos...
if not exist "fly.toml" (
    echo ❌ fly.toml no encontrado
    pause
    exit /b 1
)
if not exist "Dockerfile" (
    echo ❌ Dockerfile no encontrado
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo ❌ requirements.txt no encontrado
    pause
    exit /b 1
)
echo ✅ Archivos verificados
echo.

REM Leer nombre de app
echo [4/5] Configurando secrets...
set /p TELEGRAM_TOKEN="Ingresa tu TOKEN de Telegram: "
if "%TELEGRAM_TOKEN%"=="" (
    echo ❌ Token no puede estar vacio
    pause
    exit /b 1
)

fly secrets set TELEGRAM_BOT_TOKEN=%TELEGRAM_TOKEN%
if %errorlevel% neq 0 (
    echo ❌ Error al configurar secrets
    pause
    exit /b 1
)
echo ✅ Secrets configurados
echo.

REM Deploy
echo [5/5] Iniciando deploy...
fly deploy --remote-only
if %errorlevel% neq 0 (
    echo ❌ Error en deploy
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════╗
echo    ✅ ¡Deploy completado!
echo ╚═══════════════════════════════════════════════╝
echo.
echo Verificando estado...
fly status

echo.
echo 🔗 Tu bot esta en: https://iadaily-bot.fly.dev
echo.
echo Comandos utiles:
echo    fly status - Ver estado
echo    fly logs - Ver logs
echo    fly restart - Reiniciar
echo.
pause
