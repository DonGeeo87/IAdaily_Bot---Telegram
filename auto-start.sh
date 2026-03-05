#!/data/data/com.termux/files/usr/bin/bash
# 🚀 Auto-Start Bot - Se ejecuta al iniciar Termux
# Este script inicia automáticamente el bot

cd ~/telegram-ia-bot

echo "╔═══════════════════════════════════════════════╗"
echo "   🤖 IA Daily Bot - Auto-Iniciando"
echo "╚═══════════════════════════════════════════════╝"
echo ""

# Verificar si ya está corriendo
if pgrep -f "bot_robusto.py" > /dev/null; then
    echo "⚠️  El bot ya está corriendo"
    ps aux | grep "bot_robusto" | grep -v grep
else
    echo "🚀 Iniciando Bot Principal..."
    nohup python bot_robusto.py > logs/bot.log 2>&1 &
    sleep 3
    
    if pgrep -f "bot_robusto.py" > /dev/null; then
        echo "✅ Bot Principal iniciado"
    else
        echo "❌ Error al iniciar Bot Principal"
    fi
fi

# Verificar scheduler
if pgrep -f "master_scheduler.py" > /dev/null; then
    echo "⚠️  Scheduler ya está corriendo"
else
    echo "🚀 Iniciando Master Scheduler..."
    nohup python master_scheduler.py > logs/scheduler.log 2>&1 &
    sleep 3
    
    if pgrep -f "master_scheduler.py" > /dev/null; then
        echo "✅ Master Scheduler iniciado"
    else
        echo "❌ Error al iniciar Scheduler"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Auto-Start Completado"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Procesos activos:"
ps aux | grep "python" | grep -v grep
echo ""
echo "💡 Para ver logs: tail -f logs/bot.log"
echo ""
