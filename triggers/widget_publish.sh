#!/data/data/com.termux/files/usr/bin/bash
# 🔔 Script para Termux:Widget - Publicar post inmediatamente
# Guarda este script en ~/.termux/widget/

cd ~/telegram-ia-bot

# Generar y publicar contenido
python content_generator.py
python scheduler.py &

# Notificación
termux-notification --title "IA Daily Bot" --content "🤖 Publicando contenido..." --id 1

echo "✅ Post iniciado desde widget"
