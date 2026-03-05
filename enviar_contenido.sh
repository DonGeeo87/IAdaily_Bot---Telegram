#!/bin/bash
# 📤 MASTER SCRIPT - Generar y enviar contenido para redes
# Ejecutar: bash enviar_contenido.sh

set -e

echo "╔═══════════════════════════════════════════════╗"
echo "   📤 IA Daily - Generador de Contenido Multi-Red"
echo "╚═══════════════════════════════════════════════╝"
echo ""

cd ~/telegram-ia-bot

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Paso 1: Generar contenido nuevo
print_step "1/3 Generando contenido de IA..."
python content_generator.py
print_success "Contenido generado"
echo ""

# Paso 2: Publicar en Telegram
print_step "2/3 Publicando en canal de Telegram..."
python -c "
from telegram import Bot
import asyncio
import os

TOKEN = '8627686733:AAGgyqXtPu1juP1hjGZbb0iIhJWhq2WN324'
CHANNEL = '@IADailyChannel'

async def publicar():
    bot = Bot(token=TOKEN)
    
    # Leer primer post (herramienta)
    posts = ['herramienta', 'tip']
    for post_type in posts:
        try:
            with open(f'posts/20260304_{post_type}.txt', 'r') as f:
                post = f.read()
            
            await bot.send_message(
                chat_id=CHANNEL,
                text=post,
                parse_mode='HTML'
            )
            print(f'   ✅ Publicado: {post_type}')
        except Exception as e:
            print(f'   ⚠️  Error en {post_type}: {e}')

asyncio.run(publicar())
"
print_success "Contenido publicado en Telegram"
echo ""

# Paso 3: Enviar contenido formateado al usuario
print_step "3/3 Enviando contenido formateado a tu Telegram..."
python content_dispatcher.py
echo ""

echo "╔═══════════════════════════════════════════════╗"
echo "   ✅ ¡Todo listo!"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "📱 REVISIONES:"
echo ""
echo "1. Abre Telegram y busca @IADaily_Bot"
echo "2. Revisa los mensajes que te envió el bot"
echo "3. Copia cada post y pégalo en la red correspondiente"
echo ""
echo "📂 ARCHIVOS GENERADOS:"
ls -lh posts/*.txt 2>/dev/null | tail -5
echo ""
echo "🔗 ENLACES PARA PUBLICAR:"
echo "   Reddit:    reddit.com/submit"
echo "   Twitter:   twitter.com/home"
echo "   LinkedIn:  linkedin.com/feed"
echo "   Instagram: instagram.com"
echo "   Facebook:  facebook.com"
echo "   TikTok:    tiktok.com/upload"
echo ""
