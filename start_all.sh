#!/bin/bash
# 🚀 Start All - Inicia TODA la automatización del bot
# Ejecutar: bash start_all.sh

set -e

echo "╔═══════════════════════════════════════════════╗"
echo "   🚀 IA Daily - Iniciando Automatización Completa"
echo "╚═══════════════════════════════════════════════╝"
echo ""

cd ~/telegram-ia-bot

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar Python
print_info "Verificando Python..."
if ! command -v python &> /dev/null; then
    print_error "Python no encontrado"
    exit 1
fi
print_success "Python encontrado"

# Detener procesos anteriores
print_info "Deteniendo procesos anteriores..."
pkill -f "bot_robusto.py" 2>/dev/null || true
pkill -f "master_scheduler.py" 2>/dev/null || true
pkill -f "scheduler.py" 2>/dev/null || true
sleep 2
print_success "Procesos anteriores detenidos"

# Iniciar Bot Principal
print_info "Iniciando Bot Principal..."
nohup python bot_robusto.py > logs/bot.log 2>&1 &
sleep 3
if pgrep -f "bot_robusto.py" > /dev/null; then
    print_success "Bot Principal iniciado"
else
    print_error "Error al iniciar Bot Principal"
    exit 1
fi

# Iniciar Master Scheduler
print_info "Iniciando Master Scheduler..."
nohup python master_scheduler.py > logs/scheduler.log 2>&1 &
sleep 3
if pgrep -f "master_scheduler.py" > /dev/null; then
    print_success "Master Scheduler iniciado"
else
    print_error "Error al iniciar Master Scheduler"
    exit 1
fi

# Verificar procesos
echo ""
print_info "Verificando procesos..."
echo ""
ps aux | grep "python.*bot" | grep -v grep || true
echo ""

# Resumen
echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "   ✅ AUTOMATIZACIÓN COMPLETA INICIADA"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "📅 ACTIVIDADES PROGRAMADAS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   08:00 🛠️  Herramienta IA"
echo "   10:00 🏆  Desafío del día"
echo "   12:00 📰  Noticia IA"
echo "   14:00 📊  Encuesta diaria"
echo "   16:00 💡  Tip/Prompt"
echo "   16:30 💬  Pregunta engagement"
echo "   20:00 📦  Recurso gratuito"
echo "   Vie 18:00 🧠 Quiz semanal"
echo ""
echo "🎉 BIENVENIDA AUTOMÁTICA:"
echo "   ✅ Nuevos miembros reciben mensaje personalizado"
echo ""
echo "📊 COMANDOS ÚTILES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "   Ver logs: tail -f logs/bot.log"
echo "   Ver scheduler: tail -f logs/scheduler.log"
echo "   Ver procesos: ps aux | grep python"
echo "   Detener todo: bash stop_all.sh"
echo ""
echo "🔗 CANAL:"
echo "   @IADailyChannel"
echo ""
echo "🤖 BOT:"
echo "   @IADaily_Bot"
echo ""
print_success "¡Todo está funcionando! 🚀"
echo ""
