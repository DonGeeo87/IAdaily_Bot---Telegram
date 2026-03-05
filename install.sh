#!/bin/bash
# 🚀 Script de instalación automática para IA Daily Bot
# Ejecutar: bash install.sh

set -e

echo "🤖 ===================================="
echo "   IA Daily Bot - Instalador"
echo "===================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar Python
print_info "Verificando Python..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python no encontrado. Instalando..."
    pkg install python -y
    print_success "Python instalado"
fi

# Verificar pip
print_info "Verificando pip..."
if ! command -v pip &> /dev/null; then
    print_warning "pip no encontrado. Instalando..."
    python -m ensurepip --upgrade
fi

# Instalar dependencias
print_info "Instalando dependencias..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Dependencias instaladas"
else
    print_error "Error al instalar dependencias"
    exit 1
fi

# Crear directorios si no existen
print_info "Verificando directorios..."
mkdir -p posts logs triggers
print_success "Directorios listos"

# Verificar config.json
print_info "Verificando configuración..."
if [ ! -f config.json ]; then
    print_error "config.json no encontrado"
    exit 1
fi

# Verificar si el token fue configurado
TOKEN=$(grep -o '"bot_token": "[^"]*"' config.json | cut -d'"' -f4)
if [ "$TOKEN" = "TU_TOKEN_AQUI" ]; then
    print_warning "⚠️  El token NO ha sido configurado"
    echo ""
    echo "📝 Para configurar el bot, edita config.json:"
    echo "   1. nano config.json"
    echo "   2. Reemplaza TU_TOKEN_AQUI con tu token de BotFather"
    echo "   3. Cambia @TU_CANAL_ID por tu canal"
    echo ""
else
    print_success "Token configurado correctamente"
fi

# Crear archivo de ejemplo para posts
print_info "Generando posts de ejemplo..."
python content_generator.py

# Resumen final
echo ""
echo "🤖 ===================================="
print_success "¡Instalación completada!"
echo "===================================="
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1️⃣  Configura tu token en config.json"
echo "   nano config.json"
echo ""
echo "2️⃣  Crea tu bot en Telegram con @BotFather"
echo "   - Envía /newbot"
echo "   - Elige nombre: IA Daily"
echo "   - Elige username: IADaily_Bot"
echo "   - Copia el TOKEN"
echo ""
echo "3️⃣  Crea un canal y añade el bot como ADMIN"
echo ""
echo "4️⃣  Inicia el scheduler:"
echo "   python scheduler.py"
echo ""
echo "5️⃣  (Opcional) Ejecuta en segundo plano con tmux:"
echo "   tmux new -s iabot"
echo "   python scheduler.py"
echo "   # Ctrl+B, luego D para salir"
echo ""
echo "📚 Más info en README.md"
echo ""
print_info "¡Listo para publicar contenido de IA! 🚀"
echo ""
