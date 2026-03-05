#!/bin/bash
# 🚀 Deploy a fly.io - Script automático
# Uso: bash deploy_fly.sh

set -e

echo "╔═══════════════════════════════════════════════╗"
echo "   🚀 IA Daily Bot - Deploy a fly.io"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }

# Verificar flyctl
print_info "Verificando flyctl..."
if ! command -v fly &> /dev/null; then
    print_error "flyctl no encontrado"
    echo ""
    echo "📦 Instalar flyctl:"
    echo "   Windows: winget install fly.flyctl"
    echo "   Mac: brew install flyctl"
    echo "   Linux: curl -L https://fly.io/install.sh | sh"
    exit 1
fi
print_success "flyctl encontrado: $(fly version)"

# Verificar autenticación
print_info "Verificando autenticación..."
if ! fly auth whoami &> /dev/null; then
    print_warning "No has iniciado sesión en fly.io"
    echo ""
    print_info "Iniciando sesión..."
    fly auth login
fi
print_success "Sesión activa"

# Verificar archivos necesarios
print_info "Verificando archivos..."
for file in "fly.toml" "Dockerfile" "requirements.txt" "bot_robusto.py"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo faltante: $file"
        exit 1
    fi
done
print_success "Archivos verificados"

# Leer nombre de app desde fly.toml
APP_NAME=$(grep "^app = " fly.toml | cut -d'"' -f2)
print_info "App: $APP_NAME"

# Crear app si no existe
if ! fly status --app $APP_NAME &> /dev/null; then
    print_warning "La app no existe en fly.io, creándola..."
    fly launch --no-deploy --region mad --name $APP_NAME
fi

# Configurar secrets (variables sensibles)
print_info "Configurando secrets..."
echo ""
print_warning "Ingresa tu TOKEN de Telegram:"
read -p "TOKEN: " TELEGRAM_TOKEN
echo ""
print_info "Configurando secrets..."
fly secrets set TELEGRAM_BOT_TOKEN="$TELEGRAM_TOKEN"

# Deploy
echo ""
print_info "Iniciando deploy..."
fly deploy --remote-only

# Verificar estado
echo ""
print_info "Verificando estado..."
fly status

# Logs
echo ""
print_info "Viendo logs (Ctrl+C para salir)..."
fly logs --max 50

echo ""
echo "╔═══════════════════════════════════════════════╗"
print_success "¡Deploy completado!"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "📊 Tu bot está en: https://$APP_NAME.fly.dev"
echo ""
echo "🔧 Comandos útiles:"
echo "   fly status - Ver estado"
echo "   fly logs - Ver logs en tiempo real"
echo "   fly ssh console - Consola SSH"
echo "   fly scale count 2 - Escalar a 2 instancias"
echo ""
