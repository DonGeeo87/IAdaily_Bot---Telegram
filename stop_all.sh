#!/bin/bash
# 🛑 Stop All - Detiene toda la automatización
# Ejecutar: bash stop_all.sh

echo "🛑 Deteniendo toda la automatización..."

cd ~/telegram-ia-bot

# Detener procesos
pkill -f "bot_robusto.py" 2>/dev/null && echo "✅ Bot Principal detenido" || echo "⚠️  Bot Principal no estaba corriendo"
pkill -f "master_scheduler.py" 2>/dev/null && echo "✅ Master Scheduler detenido" || echo "⚠️  Master Scheduler no estaba corriendo"
pkill -f "scheduler.py" 2>/dev/null && echo "✅ Scheduler detenido" || echo "⚠️  Scheduler no estaba corriendo"

sleep 2

# Verificar
echo ""
if pgrep -f "python.*bot" > /dev/null; then
    echo "⚠️  Aún hay procesos de Python corriendo"
    ps aux | grep "python.*bot" | grep -v grep
else
    echo "✅ Todos los procesos detenidos"
fi

echo ""
echo "💡 Para reiniciar: bash start_all.sh"
