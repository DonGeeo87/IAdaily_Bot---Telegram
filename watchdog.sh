#!/data/data/com.termux/files/usr/bin/bash
# 🐕 Watchdog - Monitor y reinicia el bot automáticamente
# Se ejecuta cada 5 minutos para verificar que todo esté corriendo

cd ~/telegram-ia-bot

LOG_FILE="logs/watchdog.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
}

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "Iniciando verificación..."

# Verificar Bot Principal
if pgrep -f "bot_robusto.py" > /dev/null; then
    log "✅ Bot Principal: CORRIENDO"
else
    log "❌ Bot Principal: DETENIDO - Reiniciando..."
    nohup python bot_robusto.py > logs/bot.log 2>&1 &
    sleep 3
    
    if pgrep -f "bot_robusto.py" > /dev/null; then
        log "✅ Bot Principal: REINICIADO"
    else
        log "❌ Bot Principal: ERROR al reiniciar"
    fi
fi

# Verificar Scheduler
if pgrep -f "master_scheduler.py" > /dev/null; then
    log "✅ Scheduler: CORRIENDO"
else
    log "❌ Scheduler: DETENIDO - Reiniciando..."
    nohup python master_scheduler.py > logs/scheduler.log 2>&1 &
    sleep 3
    
    if pgrep -f "master_scheduler.py" > /dev/null; then
        log "✅ Scheduler: REINICIADO"
    else
        log "❌ Scheduler: ERROR al reiniciar"
    fi
fi

# Verificar uso de memoria
MEMORY=$(ps aux | grep "bot_robusto" | grep -v grep | awk '{print $4}')
if [ ! -z "$MEMORY" ]; then
    log "📊 Uso de memoria: ${MEMORY}%"
    
    # Si usa más de 50% de RAM, reiniciar
    if (( $(echo "$MEMORY > 50" | bc -l 2>/dev/null || echo 0) )); then
        log "⚠️  Uso de memoria alto - Reiniciando..."
        pkill -f "bot_robusto.py"
        sleep 2
        nohup python bot_robusto.py > logs/bot.log 2>&1 &
        log "✅ Bot reiniciado por uso de memoria"
    fi
fi

# Limpiar logs antiguos (más de 7 días)
find logs/ -name "*.log" -mtime +7 -delete 2>/dev/null
log "🧹 Logs antiguos limpiados"

log "Verificación completada"
log ""
