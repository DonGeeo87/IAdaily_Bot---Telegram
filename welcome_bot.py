#!/usr/bin/env python3
"""
🎉 Welcome Bot - Bienvenida automática a nuevos miembros del canal
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

try:
    from telegram import Bot, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, ChatMemberHandler, ContextTypes
except ImportError:
    print("Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot, ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, ChatMemberHandler, ContextTypes

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"welcome_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WelcomeBot:
    """Bienvenida automática a nuevos miembros"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = Bot(token=self.token)
        
        # Mensajes de bienvenida aleatorios
        self.welcome_messages = [
            """
🎉 **¡Bienvenido/a {name}!**

Qué alegría tenerte en **{channel}** 🤖

Aquí encontrarás:
📰 Noticias de IA diarias
🛠️ Herramientas nuevas
💡 Tips y prompts
📦 Recursos gratuitos

👇 **Empieza aquí:**
• Activa las notificaciones 🔔
• Revisa los mensajes fijados 📌
• Invita a tus amigos 👥

¡Esperamos que disfrutes! 🚀
            """,
            """
👋 **¡Hola {name}!**

Bienvenido/a a **{channel}** 🎊

Somos una comunidad de entusiastas de la IA.

📌 **Qué esperar:**
• 4 posts diarios de contenido
• Herramientas 100% verificadas
• Cero spam, solo valor

💬 **Participa:**
• Reacciona a los posts ❤️
• Comparte con amigos 🔄
• Comenta tus experiencias 💭

¡Bienvenido/a a bordo! 🚀
            """,
            """
🤖 **¡Nuevo miembro en la nave!**

Bienvenido/a {name} a **{channel}** ✨

Prepárate para:
🧠 Aprender sobre IA
⚡ Descubrir herramientas increíbles
🎯 Mejorar tu productividad

📚 **Recursos destacados:**
• Mensajes fijados (guías)
• Prompts listos para usar
• Herramientas gratuitas

¡Activa 🔔 para no perderte nada!
            """,
            """
🎊 **¡Bienvenido/a {name}!**

Gracias por unirte a **{channel}** 🙌

Somos {members} miembros apasionados por la IA.

🎯 **Tu beneficio:**
• Contenido curado diariamente
• Herramientas probadas
• Comunidad activa

💡 **Tip:** Revisa los últimos 5 posts para empezar con el pie derecho!

¡Disfruta la comunidad! 🚀
            """
        ]
    
    def load_config(self) -> dict:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def welcome_new_member(self, update: ChatMemberUpdated, context: ContextTypes.DEFAULT_TYPE):
        """Manejar nuevos miembros"""
        new_status = update.new_chat_member.status
        old_status = update.old_chat_member.status
        
        # Solo saludar si es nuevo miembro (no si era administrador, etc.)
        if new_status in ['member', 'administrator'] and old_status not in ['member', 'administrator']:
            user = update.new_chat_member.user
            channel_name = self.channel.replace('@', '')
            
            # Obtener contador de miembros
            try:
                chat = await self.bot.get_chat(self.channel)
                members_count = chat.members_count
            except:
                members_count = "?"
            
            # Seleccionar mensaje aleatorio
            import random
            welcome_text = random.choice(self.welcome_messages)
            
            # Personalizar mensaje
            welcome_text = welcome_text.format(
                name=user.mention_html(user.first_name),
                channel=self.channel,
                members=members_count
            )
            
            # Botones de acción
            keyboard = [
                [
                    InlineKeyboardButton("📌 Mensajes Fijados", url=f"https://t.me/{channel_name}"),
                    InlineKeyboardButton("👥 Invitar Amigos", url=f"https://t.me/share/url?url=https://t.me/{channel_name}")
                ],
                [
                    InlineKeyboardButton("💬 Grupo de Chat", url=f"https://t.me/{channel_name}"),
                    InlineKeyboardButton("🎯 Último Post", url=f"https://t.me/{channel_name}")
                ]
            ]
            
            try:
                await self.bot.send_message(
                    chat_id=user.id,
                    text=welcome_text,
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                logger.info(f"✅ Bienvenida enviada a {user.first_name} (@{user.username or 'N/A'})")
            except Exception as e:
                logger.error(f"❌ Error al enviar bienvenida: {e}")
    
    def get_handler(self):
        """Obtener handler para el bot"""
        return ChatMemberHandler(self.welcome_new_member, ChatMemberHandler.CHAT_MEMBER)


async def test_welcome():
    """Probar sistema de bienvenida"""
    print("🎉 Welcome Bot listo para nuevos miembros!")
    print("   El bot saludará automáticamente a cada nuevo miembro.")


if __name__ == '__main__':
    import asyncio
    asyncio.run(test_welcome())
