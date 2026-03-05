#!/usr/bin/env python3
"""
🤖 IA Daily Bot - Versión ROBUSTA con SEGURIDAD
Con integración de APIs gratuitas y sistema de permisos
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
API_CONFIG_FILE = BASE_DIR / "apis_config.json"
LOGS_DIR = BASE_DIR / "logs"
POSTS_DIR = BASE_DIR / "posts"

# Asegurar directorios
LOGS_DIR.mkdir(exist_ok=True)
POSTS_DIR.mkdir(exist_ok=True)

# Logs - Configurar PRIMERO
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"bot_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Instalar dependencias si faltan
try:
    from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        ContextTypes,
        filters,
        CallbackQueryHandler
    )
except ImportError:
    print("❌ Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
    from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

try:
    import aiohttp
except ImportError:
    print("❌ Instalando aiohttp...")
    os.system("pip install aiohttp")
    import aiohttp

# Importar sistema de seguridad
from security_manager import security, check_permission, get_role_name

# Importar Qwen AI
try:
    from qwen_ai import get_qwen_client, load_qwen_config
except ImportError:
    logger.warning("qwen_ai.py no encontrado")

# Importar Welcome Bot
try:
    from welcome_bot import WelcomeBot
except ImportError:
    logger.warning("welcome_bot.py no encontrado")

# Importar Engagement Bot
try:
    from engagement_bot import EngagementBot
except ImportError:
    logger.warning("engagement_bot.py no encontrado")


# ========== UTILIDADES DE FORMATO ==========

def md(text: str) -> str:
    """Mantiene texto con formato Markdown para Telegram"""
    return text


# ========== DECORADOR DE PERMISOS ==========

def require_permission(required_level: int):
    """Decorator para verificar permisos"""
    def decorator(func):
        async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = update.effective_user.id
            username = update.effective_user.username or str(user_id)
            command = func.__name__
            
            # Verificar permisos
            if not check_permission(user_id, command):
                user_level = security.get_user_level(user_id)
                role = get_role_name(user_id)
                
                denied_msg = f"""
⛔ **Acceso Denegado**

👤 Usuario: @{username}
🔐 Tu rol: **{role}**
📋 Comando: `/{command}`

🔒 **Nivel requerido:** {required_level}
📊 **Tu nivel:** {user_level}

💡 *Contacta a un admin para obtener acceso*
                """
                
                await update.message.reply_text(denied_msg, parse_mode='Markdown')
                
                # Log de acceso denegado
                security.log_access(user_id, username, command, False)
                logger.warning(f"⛔ Acceso denegado: @{username} ({user_id}) - {command}")
                
                return
            
            # Log de acceso permitido
            security.log_access(user_id, username, command, True)
            logger.info(f"✅ Acceso permitido: @{username} ({user_id}) - {command}")
            
            return await func(self, update, context, *args, **kwargs)
        
        return wrapper
    return decorator


# ========== RECOMENDACIONES DE IAS ==========

AI_PLATFORMS = [
    {"name": "ChatGPT", "url": "https://chat.openai.com", "desc": "El más popular. Ideal para texto y código."},
    {"name": "Claude", "url": "https://claude.ai", "desc": "Excelente para análisis y escritura larga."},
    {"name": "Gemini", "url": "https://gemini.google.com", "desc": "De Google. Multimodal nativo."},
    {"name": "Qwen", "url": "https://chat.qwen.ai", "desc": "De Alibaba. Muy bueno en español."},
    {"name": "DeepSeek", "url": "https://chat.deepseek.com", "desc": "Especializado en código y matemáticas."},
    {"name": "MiniMax", "url": "https://www.minimax.io", "desc": "IA china con razonamiento avanzado."},
    {"name": "Ollama", "url": "https://ollama.ai", "desc": "Modelos locales. Privacidad total."},
    {"name": "Perplexity", "url": "https://perplexity.ai", "desc": "Búsqueda con IA. Fuentes reales."},
    {"name": "Midjourney", "url": "https://midjourney.com", "desc": "El mejor para generar imágenes."},
    {"name": "Runway", "url": "https://runwayml.com", "desc": "Video y edición con IA."},
    {"name": "ElevenLabs", "url": "https://elevenlabs.io", "desc": "Voces sintéticas realistas."},
    {"name": "Suno", "url": "https://suno.ai", "desc": "Genera música con IA."},
    {"name": "Gamma", "url": "https://gamma.app", "desc": "Presentaciones automáticas."},
    {"name": "Notion AI", "url": "https://notion.so/ai", "desc": "IA integrada en tus notas."},
    {"name": "Cursor", "url": "https://cursor.sh", "desc": "Editor de código con IA."},
]


class IADailyBotRobusto:
    """Bot robusto con múltiples APIs"""
    
    def __init__(self):
        self.config = self.load_config()
        self.apis = self.load_apis_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = None
        self.application = None
        self.session = None

    def load_config(self) -> dict:
        """Cargar configuración principal con soporte para variables de entorno"""
        # Intentar cargar desde config_loader (variables de entorno)
        try:
            from config_loader import load_config_with_env, validate_config
            config = load_config_with_env(str(CONFIG_FILE))
            
            # Validar configuración
            valid, msg = validate_config(config)
            if not valid:
                logger.error(f"❌ Configuración inválida:\n{msg}")
                sys.exit(1)
            
            logger.info("✅ Configuración cargada (archivo + variables de entorno)")
            return config
            
        except ImportError:
            logger.warning("config_loader.py no encontrado, usando config.json directamente")
        
        # Fallback a config.json tradicional
        if not CONFIG_FILE.exists():
            logger.error("❌ config.json no encontrado")
            sys.exit(1)

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_apis_config(self) -> dict:
        """Cargar configuración de APIs"""
        default_config = {
            "gnews": {
                "api_key": "TU_API_KEY_AQUI",
                "enabled": False,
                "endpoint": "https://gnews.io/api/v4/top-headlines",
                "rate_limit": "100 req/día"
            },
            "huggingface": {
                "api_key": "TU_API_KEY_AQUI",
                "enabled": False,
                "endpoint": "https://api-inference.huggingface.co/models",
                "model": "google/flan-t5-large",
                "rate_limit": "30k req/mes"
            },
            "pexels": {
                "api_key": "TU_API_KEY_AQUI",
                "enabled": False,
                "endpoint": "https://api.pexels.com/v1/search",
                "rate_limit": "Unlimited"
            },
            "quotable": {
                "enabled": True,
                "endpoint": "http://api.quotable.io/random",
                "rate_limit": "Unlimited"
            },
            "wikipedia": {
                "enabled": True,
                "endpoint": "https://es.wikipedia.org/api/rest_v1/page/random/summary",
                "rate_limit": "Unlimited"
            }
        }
        
        if API_CONFIG_FILE.exists():
            with open(API_CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                # Merge con defaults
                for key in default_config:
                    if key in saved_config:
                        default_config[key].update(saved_config[key])
        
        return default_config
    
    def save_apis_config(self):
        """Guardar configuración de APIs"""
        with open(API_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.apis, f, indent=2, ensure_ascii=False)
        logger.info("✅ APIs config guardada")
    
    async def get_session(self):
        """Obtener sesión aiohttp"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close_session(self):
        """Cerrar sesión"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    # ========== COMANDOS PRINCIPALES ==========
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user_id = update.effective_user.id
        
        # Registrar como owner si es el primer usuario
        if not security.get_owner():
            security.set_owner(user_id)
            welcome = f"""
🎉 **¡PRIMER USUARIO DETECTADO!**

Has sido registrado como **OWNER** del bot.

👤 Tu ID: `{user_id}`
🔐 Rol: **Owner** (nivel 100)

📌 **Comandos de seguridad:**
/security - Ver configuración
/grant [user] [rol] - Dar permisos
/users - Ver todos los usuarios

🤖 **IA REAL (Qwen) - SOLO OWNER:**
/qwen [pregunta] - Chat con IA
/qwennews [tema] - Generar noticia
/qwentool [nombre] - Review herramienta
/qwenprompt [cat] - Generar prompt

🚀 **Siguiente paso:**
Configura APIs con /setup
            """
        else:
            # Usuario normal
            role = get_role_name(user_id)
            welcome = f"""
👋 ¡Hola! Soy **{self.config['branding']['bot_name']}**

{self.config['branding']['tagline']}

🔐 **Tu rol:** {role}
👤 **Tu ID:** `{user_id}`

🎯 **Este bot puede:**
• Generar contenido de IA automáticamente
• Obtener noticias en tiempo real
• Crear campañas de promoción
• Darte prompts de ChatGPT
• Y mucho más...

👇 **Usa los botones de abajo** 👇
            """
        
        keyboard = [
            [
                InlineKeyboardButton("🤖 Recomendar IA", callback_data="recomendar"),
                InlineKeyboardButton("📰 Noticias", callback_data="noticias")
            ],
            [
                InlineKeyboardButton("🚀 Campaña", callback_data="campana"),
                InlineKeyboardButton("🎯 Prompts IA", callback_data="prompts")
            ],
            [
                InlineKeyboardButton("📊 Stats", callback_data="stats"),
                InlineKeyboardButton("❓ Ayuda", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        logger.info(f"Usuario {user_id} inició el bot")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar clicks en botones"""
        query = update.callback_query
        await query.answer("Procesando...")
        
        action = query.data
        chat_id = query.message.chat_id if query.message else None
        
        logger.info(f"🔘 Botón presionado: {action}")
        
        try:
            if action == "recomendar":
                await self.recomendar(update, context, chat_id)
            elif action == "noticias":
                await self.noticias(update, context, chat_id)
            elif action == "campana":
                await self.campana(update, context, chat_id)
            elif action == "prompts":
                await self.prompts(update, context, chat_id)
            elif action == "stats":
                await self.stats(update, context, chat_id)
            elif action == "help":
                await self.help_command(update, context, chat_id)
            elif action == "analytics_refresh":
                await self.analytics_command(update, context, chat_id)
            elif action == "analytics_30d":
                await self.analytics_command(update, context, chat_id)
            elif action == "modelos":
                await self.modelos_command(update, context, chat_id)
            elif action == "ver_campaign":
                await self.ver_campaign(update, context, chat_id)
            else:
                await query.edit_message_text(f"⚠️ Botón desconocido: {action}")
                logger.warning(f"⚠️  Acción desconocida: {action}")
        except Exception as e:
            logger.error(f"❌ Error en botón {action}: {e}")
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {e}")

    async def recomendar(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Recomendar plataforma de IA al azar"""
        import random

        ai = random.choice(AI_PLATFORMS)

        mensaje = f"""
🤖 **IA Recomendada del Día**

📌 **{ai['name']}**

{ai['desc']}

🔗 **Enlace:** {ai['url']}

💡 *¿Quieres otra recomendación?*
Presiona el botón nuevamente.
        """
        
        if chat_id:
            await context.bot.send_message(chat_id=chat_id, text=mensaje, parse_mode='Markdown')
        else:
            await update.message.reply_text(mensaje, parse_mode='Markdown')

    async def generar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generar contenido de IA"""
        msg = await update.message.reply_text(
            "🤖 **Generando contenido de IA...**\n\n"
            "Esto puede tomar unos segundos.",
            parse_mode='Markdown'
        )
        
        try:
            import subprocess
            result = subprocess.run(
                ['python', str(BASE_DIR / 'content_generator.py')],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR)
            )
            
            if result.returncode == 0:
                posts_dir = BASE_DIR / 'posts'
                today = datetime.now().strftime("%Y%m%d")
                
                mensaje = "✅ **Contenido generado exitosamente!**\n\n"
                
                for post_type in ['herramienta', 'noticia', 'tip', 'recurso', 'prompt']:
                    filename = posts_dir / f"{today}_{post_type}.txt"
                    if filename.exists():
                        with open(filename, 'r', encoding='utf-8') as f:
                            content = f.read()[:300]
                        emoji = {"herramienta": "🛠️", "noticia": "📰", "tip": "💡", "recurso": "📦", "prompt": "🎯"}[post_type]
                        mensaje += f"{emoji} **{post_type.title()}**\n`{content}...`\n\n"
                
                mensaje += "📁 *Archivos completos en: ~/telegram-ia-bot/posts/*"
                
                await msg.edit_text(mensaje, parse_mode='Markdown')
            else:
                await msg.edit_text(f"❌ Error al generar: {result.stderr}")
                
        except Exception as e:
            await msg.edit_text(f"❌ Error: {e}")

    async def noticias(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Obtener noticias de IA en tiempo real"""
        # Verificar si GNews está habilitado
        if not self.apis["gnews"]["enabled"] or not self.apis["gnews"]["api_key"]:
            mensaje = "📰 **Noticias de IA**\n\n"
            mensaje += "⚠️ *GNews API no configurada.*\n\n"
            mensaje += "Para activar noticias en vivo:\n"
            mensaje += "1. Obtén API key gratis en: https://gnews.io/\n"
            mensaje += "2. Usa el comando: `/setgnews TU_API_KEY`\n\n"
            mensaje += "O usa /qwennews para noticias con Qwen AI."

            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=mensaje, parse_mode='Markdown')
            else:
                await update.message.reply_text(mensaje, parse_mode='Markdown')
            return

        # Obtener noticias de GNews
        noticias_text = await self.get_gnews_noticias()

        if noticias_text:
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=noticias_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(noticias_text, parse_mode='Markdown')
        else:
            mensaje = "⚠️ No se pudieron obtener noticias en este momento.\n\nIntenta nuevamente más tarde."
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=mensaje, parse_mode='Markdown')
            else:
                await update.message.reply_text(mensaje, parse_mode='Markdown')

    async def campana(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Obtener campaña de promoción"""
        if chat_id:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🚀 **Generando campaña de promoción...**\n\nRecibirás 4 posts listos para publicar.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "🚀 **Generando campaña de promoción...**\n\nRecibirás 4 posts listos para publicar.",
                parse_mode='Markdown'
            )

        try:
            import subprocess
            result = subprocess.run(
                ['python', str(BASE_DIR / 'campaign_manager.py')],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR)
            )

            if result.returncode == 0:
                keyboard = [[InlineKeyboardButton("📁 Ver Archivos", callback_data="ver_campaign")]]
                
                mensaje = "✅ **Campaña generada exitosamente!**\n\n📁 Archivos en: `~/telegram-ia-bot/campaign/`\n\nRevisa tu Telegram para los posts completos."

                if chat_id:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=mensaje,
                        parse_mode='Markdown',
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                else:
                    await update.message.reply_text(
                        mensaje,
                        parse_mode='Markdown',
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
            else:
                error_msg = f"❌ Error: {result.stderr}" if result.stderr else "❌ Error al generar campaña"
                if chat_id:
                    await context.bot.send_message(chat_id=chat_id, text=error_msg)
                else:
                    await update.message.reply_text(error_msg)

        except Exception as e:
            error_msg = f"❌ Error: {e}"
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=error_msg)
            else:
                await update.message.reply_text(error_msg)

    async def ver_campaign(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Ver archivos de campaña disponibles"""
        try:
            today = datetime.now().strftime("%Y%m%d")
            campaign_dir = BASE_DIR / "campaign"
            
            if not campaign_dir.exists():
                msg = "⚠️ No hay directorio de campañas"
                if chat_id:
                    await context.bot.send_message(chat_id=chat_id, text=msg)
                else:
                    await update.message.reply_text(msg)
                return
            
            # Buscar archivos de hoy
            archivos = list(campaign_dir.glob(f"{today}_*.txt"))
            
            if not archivos:
                msg = "⚠️ No hay campañas generadas para hoy.\n\nUsa el botón 🚀 Campaña para generar una nueva."
                if chat_id:
                    await context.bot.send_message(chat_id=chat_id, text=msg)
                else:
                    await update.message.reply_text(msg)
                return
            
            msg = "📁 **Campañas Disponibles**\n\n"
            keyboard = []
            
            for archivo in archivos:
                nombre = archivo.stem.replace(f"{today}_", "").replace("_", " ").title()
                msg += f"📄 **{nombre}**\n"
                keyboard.append([InlineKeyboardButton(f"📄 {nombre}", callback_data=f"leer_{archivo.name}")])
            
            if chat_id:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await update.message.reply_text(
                    msg,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                
        except Exception as e:
            error_msg = f"❌ Error: {e}"
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=error_msg)
            else:
                await update.message.reply_text(error_msg)

    async def prompts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Obtener prompts para TODAS las IAs"""
        import random

        prompts_list = {
            "🟢 ChatGPT": [
                "Actúa como [rol experto]. Crea [contenido] para [audiencia]. Incluye [elementos].",
                "Explica [concepto] como si tuviera 10 años. Usa analogías y ejemplos.",
                "Escribe código en [lenguaje] para [función]. Con comentarios y tests.",
            ],
            "🔵 Claude": [
                "Analiza este texto en profundidad: [TEXTO]. Extrae argumentos, sesgos y conclusiones.",
                "Resume este documento largo manteniendo los puntos clave: [DOCUMENTO]",
                "Escribe un ensayo estructurado sobre [tema] con introducción, desarrollo y conclusión.",
            ],
            "🟣 Gemini": [
                "Compara [producto A] vs [producto B]. Incluye tabla comparativa y recomendación.",
                "Genera ideas creativas para [proyecto]. Mínimo 10 ideas diferentes.",
                "Analiza esta imagen: [DESCRIPCIÓN]. ¿Qué ves? ¿Qué significa?",
            ],
            "🟠 Qwen": [
                "Traduce este texto al español manteniendo el tono: [TEXTO]",
                "Escribe contenido optimizado para SEO sobre [palabra clave].",
                "Genera una conversación entre [personaje 1] y [personaje 2] sobre [tema].",
            ],
            "🔷 DeepSeek": [
                "Resuelve este problema matemático paso a paso: [PROBLEMA]",
                "Optimiza este código para mejor rendimiento: [CÓDIGO]",
                "Explica este algoritmo complejo de forma simple: [ALGORITMO]",
            ],
            "🟡 MiniMax": [
                "Genera un plan de negocios para [idea]. Incluye mercado, competencia y proyecciones.",
                "Crea una estrategia de marketing para [producto]. Canales, presupuesto, KPIs.",
                "Analiza tendencias de [industria] para 2026.",
            ],
            "🦙 Ollama": [
                "Configura un modelo local para [caso de uso]. Especifica hardware necesario.",
                "Compara modelos open-source para [tarea específica].",
                "Crea un pipeline de procesamiento local con privacidad total.",
            ],
            "🎨 Midjourney": [
                "/imagine prompt: [sujeto], [estilo], [iluminación], [composición] --ar 16:9 --v 6",
                "/imagine prompt: [escena], [atmósfera], [colores], [detalle] --stylize 250",
                "/imagine prompt: [personaje], [vestimenta], [fondo], [expresión] --chaos 30",
            ],
            "🎵 Suno": [
                "Crea una canción sobre [tema]. Género: [género]. Tempo: [rápido/lento].",
                "Genera música instrumental para [ocasión]. Instrumentos: [lista].",
                "Compone una melodía pegadiza con letra sobre [historia].",
            ],
            "🎬 Runway": [
                "Genera video de [escena] con estilo [cinematográfico/animado]. Duración: 10s.",
                "Aplica efecto [nombre] a este video. Mantén calidad original.",
                "Crea transición suave entre [escena A] y [escena B].",
            ],
            "🔊 ElevenLabs": [
                "Genera narración con voz [masculina/femenina] para [guión]. Tono: [tono].",
                "Clona esta voz manteniendo emociones: [MUESTRA]. Texto: [TEXTO].",
                "Crea diálogo entre [personaje 1] y [personaje 2] con emociones distintas.",
            ],
        }

        # Seleccionar IA al azar
        ia_name = random.choice(list(prompts_list.keys()))
        prompts = prompts_list[ia_name]
        prompt_elegido = random.choice(prompts)

        mensaje = f"""
🎯 **Prompt para {ia_name}**

`{prompt_elegido}`

💡 *¿Quieres más prompts para esta IA?*
Presiona el botón de abajo.

📚 **IAs disponibles:**
ChatGPT, Claude, Gemini, Qwen, DeepSeek, MiniMax, Ollama, Midjourney, Suno, Runway, ElevenLabs
        """

        keyboard = [[InlineKeyboardButton("🔄 Otro Prompt", callback_data="prompts")]]

        if chat_id:
            await context.bot.send_message(
                chat_id=chat_id,
                text=mensaje,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                mensaje,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Ayuda completa"""
        help_text = """
📚 **AYUDA - IA Daily Bot**

🎯 **COMANDOS:**
• /start - Menú
• /recomendar - IA aleatoria
• /prompts - Prompts
• /analytics - Métricas
• /modelos - Modelos Qwen
• /qwen [pregunta] - Chat IA

📊 **INFO:**
• /stats - Estadísticas
• /help - Esta ayuda

🔧 **CONFIG:**
• /setup - Configurar APIs
"""
        if chat_id:
            await context.bot.send_message(chat_id=chat_id, text=help_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(help_text, parse_mode='Markdown')

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Estadísticas del canal"""
        try:
            bot = Bot(token=self.token)
            chat = await bot.get_chat(self.channel)
            members_count = await chat.get_member_count()

            stats_msg = f"""
📊 **Estadísticas del Canal**

📢 **Nombre:** {chat.title}
👥 **Miembros:** {members_count:,}
🔗 **Link:** {chat.invite_link if hasattr(chat, 'invite_link') else self.channel}

📈 **Actividad:**
• Posts/día: 4
• Horarios: 08:00, 12:00, 16:00, 20:00
• Estado: ✅ Activo
            """

            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=stats_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(stats_msg, parse_mode='Markdown')

        except Exception as e:
            error_msg = f"❌ Error: {e}"
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=error_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    async def get_gnews_noticias(self) -> str:
        """Obtener noticia de IA aleatoria de GNews API"""
        import random
        session = await self.get_session()

        params = {
            "q": "inteligencia artificial OR IA OR ChatGPT OR AI",
            "lang": "es",
            "country": "us",
            "apikey": self.apis["gnews"]["api_key"]
        }

        async with session.get(self.apis["gnews"]["endpoint"], params=params) as response:
            if response.status == 200:
                data = await response.json()
                articles = data.get("articles", [])
                
                if not articles:
                    return ""
                
                # Seleccionar 1 artículo al azar
                article = random.choice(articles)

                mensaje = "📰 **Noticia de IA**\n\n"
                mensaje += f"**{article['title']}**\n\n"
                descripcion = article['description'] if article['description'] else "Sin descripción"
                mensaje += f"{descripcion[:300]}\n\n"
                mensaje += f"🔗 [Leer más]({article['url']})\n\n"
                mensaje += f"📅 Publicado: {article['publishedAt']}\n"
                mensaje += f"📰 Fuente: {article['source']['name']}"

                return mensaje

        return ""
    
    async def get_wikipedia_ia(self) -> str:
        """Obtener artículo aleatorio de IA de Wikipedia"""
        session = await self.get_session()
        
        async with session.get(self.apis["wikipedia"]["endpoint"]) as response:
            if response.status == 200:
                data = await response.json()
                
                mensaje = "📚 **Sabías que...**\n\n"
                mensaje += f"**{data['title']}**\n\n"
                mensaje += f"{data['extract'][:500]}...\n\n"
                mensaje += f"🔗 [Leer en Wikipedia]({data['content_urls']['desktop']['page']})"
                
                return mensaje

        return ""

    async def setup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Configurar APIs"""
        setup_msg = """
⚙️ **CONFIGURACIÓN DE APIS**

📰 **GNews API** (Noticias en tiempo real):
1. Ve a: https://gnews.io/
2. Regístrate gratis
3. Copia tu API key
4. Ejecuta: /setgnews [TU_KEY]
🤖 **Hugging Face** (IA avanzada):
1. Ve a: https://huggingface.co/
2. Crea cuenta gratis
3. Copia tu token
4. Ejecuta: /sethf [TU_TOKEN]

📸 **Pexels** (Imágenes gratis):
1. Ve a: https://www.pexels.com/api/
2. Regístrate
3. Copia tu key
4. Ejecuta: /setpexels [TU_KEY]

✅ **APIs activas actualmente:**
        """
        
        for api_name, config in self.apis.items():
            status = "✅" if config.get("enabled", False) else "❌"
            setup_msg += f"{status} **{api_name.title()}**\n"
        
        await update.message.reply_text(setup_msg, parse_mode='Markdown')
    
    async def set_api_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Configurar API key"""
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "Uso: `/setgnews [TU_API_KEY]`\n\n"
                "Ejemplo: `/setgnews abc123xyz`",
                parse_mode='Markdown'
            )
            return
        
        api_type = context.args[0].lower()
        api_key = context.args[1]
        
        if api_type == "gnews":
            self.apis["gnews"]["api_key"] = api_key
            self.apis["gnews"]["enabled"] = True
        elif api_type == "hf":
            self.apis["huggingface"]["api_key"] = api_key
            self.apis["huggingface"]["enabled"] = True
        elif api_type == "pexels":
            self.apis["pexels"]["api_key"] = api_key
            self.apis["pexels"]["enabled"] = True
        else:
            await update.message.reply_text(f"❌ API '{api_type}' no reconocida")
            return
        
        self.save_apis_config()
        await update.message.reply_text(f"✅ **{api_type.upper()} configurado exitosamente!**", parse_mode='Markdown')
    
    # ========== COMANDOS DE GRUPO ==========
    
    async def group_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ayuda para grupos"""
        await update.message.reply_text(
            "🤖 **IA Daily Bot en Grupos**\n\n"
            "Puedes usarme para:\n\n"
            "• `/ia [tema]` - Generar contenido sobre un tema\n"
            "• `/prompt` - Obtener prompt de ChatGPT\n"
            "• `/noticia` - Noticia de IA del día\n\n"
            "📢 Canal oficial: @IADailyChannel"
        )
    
    async def ia_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Consulta de IA en grupos"""
        if not context.args:
            await update.message.reply_text(
                "Uso: `/ia [tema]`\n\n"
                "Ejemplo: `/ia ChatGPT`",
                parse_mode='Markdown'
            )
            return
        
        tema = ' '.join(context.args)
        
        respuesta = f"""
🤖 **Respuesta sobre: {tema}**

La inteligencia artificial está transformando cómo trabajamos con {tema}.

💡 **Puntos clave:**
• Las herramientas de IA pueden automatizar tareas
• Los prompts correctos mejoran resultados
• La práctica constante es esencial

📚 **Recursos:**
• ChatGPT para redacción
• Midjourney para imágenes
• Nuestro canal para más: @IADailyChannel

#IA #{tema.replace(' ', '')}
        """
        
        await update.message.reply_text(respuesta, parse_mode='Markdown')

    # ========== COMANDOS DE SEGURIDAD ==========

    @require_permission(100)
    async def security_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ver configuración de seguridad (solo owner)"""
        stats = security.get_stats()
        owner_id = security.get_owner()
        
        msg = f"""
🔐 **CONFIGURACIÓN DE SEGURIDAD**

👑 **Owner:** `{owner_id}`

📊 **Estadísticas:**
• Admins: {stats['admin_count']}
• Premium: {stats['premium_count']}
• Baneados: {stats['banned_count']}
• Grupos: {stats['group_count']}
• Logs: {stats['log_entries']}

📋 **NIVELES DE ACCESO:**
• Owner (100) - Acceso total
• Admin (50) - Comandos admin
• Premium (20) - Campañas
• User (10) - Básico
• Banned (0) - Sin acceso

🔧 **COMANDOS:**
/grant [user] [rol] - Dar permisos
/revoke [user] [rol] - Quitar permisos
/ban [user] - Banear
/unban [user] - Desbanear
/users - Ver usuarios
/log - Ver logs
        """
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    @require_permission(100)
    async def grant_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Dar permisos a usuario"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "Uso: `/grant [user_id] [rol]`\n\n"
                "Ejemplos:\n"
                "`/grant 123456789 admin`\n"
                "`/grant 123456789 premium`\n\n"
                "Roles: owner, admin, premium, user",
                parse_mode='Markdown'
            )
            return
        
        user_id = int(context.args[0])
        role = context.args[1].lower()
        
        if role == "admin":
            security.add_admin(user_id)
        elif role == "premium":
            security.add_premium(user_id)
        elif role == "owner":
            security.set_owner(user_id)
        elif role == "user":
            security.remove_admin(user_id)
            security.remove_premium(user_id)
        else:
            await update.message.reply_text(f"❌ Rol '{role}' no válido")
            return
        
        await update.message.reply_text(
            f"✅ **Permisos actualizados**\n\n"
            f"👤 Usuario: `{user_id}`\n"
            f"🔐 Nuevo rol: **{role}**",
            parse_mode='Markdown'
        )
    
    @require_permission(100)
    async def revoke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quitar permisos a usuario"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "Uso: `/revoke [user_id] [rol]`\n\n"
                "Ejemplo: `/revoke 123456789 admin`",
                parse_mode='Markdown'
            )
            return
        
        user_id = int(context.args[0])
        role = context.args[1].lower()
        
        if role == "admin":
            security.remove_admin(user_id)
        elif role == "premium":
            security.remove_premium(user_id)
        else:
            await update.message.reply_text(f"❌ Rol '{role}' no se puede revocar")
            return
        
        await update.message.reply_text(
            f"✅ **Permisos revocados**\n\n"
            f"👤 Usuario: `{user_id}`\n"
            f"🔐 Rol removido: **{role}**",
            parse_mode='Markdown'
        )
    
    @require_permission(100)
    async def ban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Banear usuario"""
        if not context.args:
            await update.message.reply_text(
                "Uso: `/ban [user_id]`\n\n"
                "Ejemplo: `/ban 123456789`",
                parse_mode='Markdown'
            )
            return
        
        user_id = int(context.args[0])
        security.ban_user(user_id)
        
        await update.message.reply_text(
            f"⛔ **Usuario BANEADO**\n\n"
            f"👤 Usuario: `{user_id}`\n\n"
            f"Este usuario ya no podrá usar el bot.",
            parse_mode='Markdown'
        )
    
    @require_permission(100)
    async def unban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Desbanear usuario"""
        if not context.args:
            await update.message.reply_text(
                "Uso: `/unban [user_id]`\n\n"
                "Ejemplo: `/unban 123456789`",
                parse_mode='Markdown'
            )
            return
        
        user_id = int(context.args[0])
        security.unban_user(user_id)
        
        await update.message.reply_text(
            f"✅ **Usuario DESBANEADO**\n\n"
            f"👤 Usuario: `{user_id}`\n\n"
            f"Este usuario puede volver a usar el bot.",
            parse_mode='Markdown'
        )
    
    @require_permission(50)
    async def users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ver todos los usuarios"""
        users = security.get_all_users()
        
        msg = "👥 **USUARIOS DEL BOT**\n\n"
        msg += f"👑 **Owner:** `{users['owner']}`\n\n"
        
        if users['admins']:
            msg += "🔧 **Admins:**\n"
            for admin_id in users['admins']:
                msg += f"  • `{admin_id}`\n"
            msg += "\n"
        
        if users['premium']:
            msg += "⭐ **Premium:**\n"
            for prem_id in users['premium']:
                msg += f"  • `{prem_id}`\n"
            msg += "\n"
        
        if users['banned']:
            msg += "⛔ **Baneados:**\n"
            for ban_id in users['banned']:
                msg += f"  • `{ban_id}`\n"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    @require_permission(50)
    async def log_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ver log de accesos"""
        limit = int(context.args[0]) if context.args else 20
        logs = security.get_access_log(limit)
        
        if not logs:
            await update.message.reply_text("📭 No hay logs registrados")
            return
        
        msg = f"📋 **ÚLTIMOS {len(logs)} ACCESOS**\n\n"
        
        for log in reversed(logs[-10:]):
            status = "✅" if log['allowed'] else "⛔"
            msg += f"{status} `{log['timestamp'].split('T')[1][:8]}` - @{log['username']} - {log['command']}\n"
        
        await update.message.reply_text(msg, parse_mode='Markdown')

    @require_permission(50)
    async def analytics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Ver analytics del canal"""
        try:
            from analytics_dashboard import AnalyticsDashboard

            dashboard = AnalyticsDashboard()
            report = dashboard.generate_report()

            keyboard = [
                [InlineKeyboardButton("🔄 Actualizar", callback_data="analytics_refresh")],
                [InlineKeyboardButton("📈 30 días", callback_data="analytics_30d")]
            ]

            if chat_id:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=report,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await update.message.reply_text(
                    report,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        except Exception as e:
            error_msg = f"❌ Error al obtener analytics: {e}"
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=error_msg)
            else:
                await update.message.reply_text(error_msg)

    # ========== MINI APP GAME COMMANDS ==========

    async def mini_app_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /juego - IA Clicker Empire Mini App"""
        try:
            from mini_app_handler import game_command
            await game_command(update, context)
        except ImportError:
            await update.message.reply_text(
                "🎮 **IA Clicker Empire**\n\n"
                "La Mini App está en mantenimiento. ¡Prueba pronto!",
                parse_mode='Markdown'
            )

    async def mini_app_trivia(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /trivia - Trivia diaria"""
        try:
            from mini_app_handler import trivia_command
            await trivia_command(update, context)
        except ImportError:
            await update.message.reply_text(
                "🧮 **Trivia IA**\n\n"
                "La trivia está en mantenimiento. ¡Prueba pronto!",
                parse_mode='Markdown'
            )

    async def mini_app_ranking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /ranking - Leaderboard"""
        try:
            from mini_app_handler import leaderboard_command
            await leaderboard_command(update, context)
        except ImportError:
            await update.message.reply_text(
                "🏆 **Ranking**\n\n"
                "El ranking está en mantenimiento. ¡Prueba pronto!",
                parse_mode='Markdown'
            )

    async def mini_app_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /perfil - Perfil del jugador"""
        try:
            from mini_app_handler import profile_command
            await profile_command(update, context)
        except ImportError:
            await update.message.reply_text(
                "👤 **Tu Perfil**\n\n"
                "El perfil está en mantenimiento. ¡Prueba pronto!",
                parse_mode='Markdown'
            )

    # ========== PANEL DE MODELOS QWEN/WAN (SOLO OWNER) ==========

    @require_permission(100)
    async def modelos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None):
        """Ver modelos disponibles con cuotas"""
        import json
        from pathlib import Path

        config_file = BASE_DIR / "modelos_config.json"
        if not config_file.exists():
            msg = "❌ No hay configuración de modelos"
            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=msg)
            else:
                await update.message.reply_text(msg)
            return

        with open(config_file, 'r') as f:
            config = json.load(f)

        msg = "🤖 **MODELOS QWEN Y WAN DISPONIBLES**\n\n"

        msg += "📝 **TEXTO:**\n"
        for modelo in config["modelos_qwen"]:
            if modelo["tipo"] == "texto":
                msg += f"• `{modelo['nombre']}` - {modelo['tokens']:,} tokens (vence: {modelo['vence']})\n"

        msg += "\n👁️ **VISIÓN:**\n"
        for modelo in config["modelos_qwen"]:
            if modelo["tipo"] == "vision":
                msg += f"• `{modelo['nombre']}` - {modelo['tokens']:,} tokens (vence: {modelo['vence']})\n"
        
        msg += "\n💻 **CÓDIGO:**\n"
        for modelo in config["modelos_qwen"]:
            if modelo["tipo"] == "codigo":
                msg += f"• `{modelo['nombre']}` - {modelo['tokens']:,} tokens (vence: {modelo['vence']})\n"
        
        msg += "\n🎭 **ROLEPLAY:**\n"
        for modelo in config["modelos_qwen"]:
            if modelo["tipo"] == "roleplay":
                msg += f"• `{modelo['nombre']}` - {modelo['tokens']:,} tokens (vence: {modelo['vence']})\n"
        
        msg += "\n🎬 **VIDEO (Wan):**\n"
        for modelo in config["modelos_wan"]:
            msg += f"• `{modelo['nombre']}` - {modelo['usos']} usos (vence: {modelo['vence']})\n"
        
        msg += "\n💡 **Usa:** `/usarmodelo [nombre] [prompt]`"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Actualizar", callback_data="modelos")]
        ]
        
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    @require_permission(100)
    async def usar_modelo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Usar un modelo específico"""
        if len(context.args) < 2:
            await update.message.reply_text(
                "🤖 **Usar Modelo**\n\n"
                "Uso: `/usarmodelo [nombre] [prompt]`\n\n"
                "Ejemplos:\n"
                "`/usarmodelo qwen3.5-397b-a17b ¿Qué es la IA?`\n"
                "`/usarmodelo qwen3-vl-plus Describe esta imagen`\n"
                "`/usarmodelo wan2.2-kf2v-flash Video de un atardecer`",
                parse_mode='Markdown'
            )
            return
        
        modelo_nombre = context.args[0]
        prompt = ' '.join(context.args[1:])
        
        # Verificar si Qwen está configurado
        qwen = get_qwen_client()
        if not qwen:
            await update.message.reply_text("❌ Qwen no configurado", parse_mode='Markdown')
            return
        
        status_msg = await update.message.reply_text(f"🤖 Usando {modelo_nombre}...")
        
        # Usar el modelo (simplificado - usa el modelo por defecto)
        response = await qwen.generate_text(prompt)
        
        await status_msg.edit_text(
            f"🤖 **{modelo_nombre}**\n\n{response}",
            parse_mode='Markdown'
        )

    # ========== COMANDOS QWEN AI (SOLO OWNER) ==========

    @require_permission(100)
    async def qwen_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Chat con IA de Qwen (solo owner)"""
        if not context.args:
            await update.message.reply_text(
                "🤖 **Chat con Qwen AI**\n\n"
                "Solo para OWNER.\n\n"
                "Uso: `/qwen [tu pregunta]`\n\n"
                "Ejemplo:\n"
                "`/qwen ¿Qué es el machine learning?`",
                parse_mode='Markdown'
            )
            return
        
        # Verificar Qwen configurado
        qwen = get_qwen_client()
        if not qwen:
            await update.message.reply_text(
                "❌ Qwen AI no está configurado.\n\n"
                "El owner debe configurar la API key en `qwen_config.json`",
                parse_mode='Markdown'
            )
            return
        
        question = ' '.join(context.args)
        
        # Mostrar "escribiendo..."
        status_msg = await update.message.reply_text("🤖 Qwen está pensando...")
        
        # Generar respuesta
        response = await qwen.chat(question)
        
        await status_msg.edit_text(
            f"🤖 **Qwen AI**\n\n{response}",
            parse_mode='Markdown'
        )
    
    @require_permission(100)
    async def qwen_news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generar noticia con Qwen (solo owner)"""
        if not context.args:
            await update.message.reply_text(
                "📰 **Generar Noticia con Qwen**\n\n"
                "Uso: `/qwennews [tema]`\n\n"
                "Ejemplo:\n"
                "`/qwennews ChatGPT`",
                parse_mode='Markdown'
            )
            return
        
        qwen = get_qwen_client()
        if not qwen:
            await update.message.reply_text("❌ Qwen no configurado", parse_mode='Markdown')
            return
        
        topic = ' '.join(context.args)
        status_msg = await update.message.reply_text("📰 Generando noticia...")
        
        response = await qwen.generate_news_summary(topic)
        
        await status_msg.edit_text(
            f"📰 **Noticia Generada por Qwen**\n\n{response}",
            parse_mode='Markdown'
        )
    
    @require_permission(100)
    async def qwen_tool(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generar review de herramienta con Qwen (solo owner)"""
        if not context.args:
            await update.message.reply_text(
                "🛠️ **Review de Herramienta con Qwen**\n\n"
                "Uso: `/qwentool [nombre]`\n\n"
                "Ejemplo:\n"
                "`/qwentool Midjourney`",
                parse_mode='Markdown'
            )
            return
        
        qwen = get_qwen_client()
        if not qwen:
            await update.message.reply_text("❌ Qwen no configurado", parse_mode='Markdown')
            return
        
        tool_name = ' '.join(context.args)
        status_msg = await update.message.reply_text("🛠️ Analizando herramienta...")
        
        response = await qwen.generate_tool_review(tool_name)
        
        await status_msg.edit_text(
            f"🛠️ **Review Generada por Qwen**\n\n{response}",
            parse_mode='Markdown'
        )
    
    @require_permission(100)
    async def qwen_prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generar prompt con Qwen (solo owner)"""
        if not context.args:
            await update.message.reply_text(
                "🎯 **Generar Prompt con Qwen**\n\n"
                "Uso: `/qwenprompt [categoría]`\n\n"
                "Ejemplo:\n"
                "`/qwenprompt productividad`",
                parse_mode='Markdown'
            )
            return
        
        qwen = get_qwen_client()
        if not qwen:
            await update.message.reply_text("❌ Qwen no configurado", parse_mode='Markdown')
            return
        
        category = ' '.join(context.args)
        status_msg = await update.message.reply_text("🎯 Creando prompt...")
        
        response = await qwen.generate_prompt_chatgpt(category)
        
        await status_msg.edit_text(
            f"🎯 **Prompt Generado por Qwen**\n\n{response}",
            parse_mode='Markdown'
        )

    # ========== GESTIÓN ==========

    def get_handlers(self):
        """Obtener todos los handlers"""
        handlers = [
            # Comandos principales
            CommandHandler('start', self.start),
            CommandHandler('recomendar', self.recomendar),
            CommandHandler('generar', self.generar),
            CommandHandler('noticias', self.noticias),
            CommandHandler('campana', self.campana),
            CommandHandler('prompts', self.prompts),
            CommandHandler('stats', self.stats),
            CommandHandler('help', self.help_command),

            # Configuración
            CommandHandler('setup', self.setup),
            CommandHandler('setgnews', self.set_api_key),
            CommandHandler('sethf', self.set_api_key),
            CommandHandler('setpexels', self.set_api_key),

            # Seguridad (Owner/Admin)
            CommandHandler('security', self.security_command),
            CommandHandler('grant', self.grant_command),
            CommandHandler('revoke', self.revoke_command),
            CommandHandler('ban', self.ban_command),
            CommandHandler('unban', self.unban_command),
            CommandHandler('users', self.users_command),
            CommandHandler('log', self.log_command),
            CommandHandler('analytics', self.analytics_command),

            # Mini App Game - IA Clicker Empire
            CommandHandler('juego', self.mini_app_game),
            CommandHandler('game', self.mini_app_game),
            CommandHandler('trivia', self.mini_app_trivia),
            CommandHandler('ranking', self.mini_app_ranking),
            CommandHandler('perfil', self.mini_app_profile),

            # Modelos Qwen/Wan (Solo Owner)
            CommandHandler('modelos', self.modelos_command),
            CommandHandler('usarmodelo', self.usar_modelo),

            # Qwen AI (Solo Owner)
            CommandHandler('qwen', self.qwen_chat),
            CommandHandler('qwennews', self.qwen_news),
            CommandHandler('qwentool', self.qwen_tool),
            CommandHandler('qwenprompt', self.qwen_prompt),

            # Grupos
            CommandHandler('ia', self.ia_query),
            CommandHandler('ayuda', self.group_help),

            # Callbacks de botones inline (SIN patrón para capturar todos)
            CallbackQueryHandler(self.button_callback),
        ]
        
        # Importar handlers adicionales de mini_app_handler
        try:
            from mini_app_handler import get_handlers as get_mini_app_handlers
            handlers.extend(get_mini_app_handlers())
        except ImportError:
            logger.warning("mini_app_handler.py no encontrado, usando handlers básicos")
        
        return handlers
    
    async def cleanup(self):
        """Limpieza al cerrar"""
        await self.close_session()
    
    async def set_commands(self, bot: Bot):
        """Configurar menú de comandos en Telegram"""
        commands = [
            BotCommand('start', '🏠 Menú principal'),
            BotCommand('juego', '🎮 IA Clicker Empire (Mini App)'),
            BotCommand('trivia', '🧠 Trivia diaria de IA'),
            BotCommand('ranking', '🏆 Ranking global'),
            BotCommand('recomendar', '🤖 IA recomendada del día'),
            BotCommand('noticias', '📰 Noticia de IA aleatoria'),
            BotCommand('prompts', '🎯 Prompt para alguna IA'),
            BotCommand('campana', '🚀 Generar campaña promoción'),
            BotCommand('stats', '📊 Estadísticas del canal'),
            BotCommand('help', '❓ Ayuda y comandos'),
            BotCommand('analytics', '📈 Analytics del bot'),
            BotCommand('modelos', '🤖 Modelos Qwen disponibles'),
            BotCommand('qwen', '💬 Chat con IA Qwen'),
            BotCommand('qwennews', '📰 Generar noticia con Qwen'),
            BotCommand('qwentool', '🛠️ Review herramienta con Qwen'),
            BotCommand('qwenprompt', '🎯 Generar prompt con Qwen'),
            BotCommand('setup', '⚙️ Configurar APIs'),
            BotCommand('security', '🔐 Configuración de seguridad'),
        ]
        await bot.set_my_commands(commands)
        logger.info("✅ Menú de comandos configurado")

    def run(self):
        """Ejecutar el bot"""
        if self.token == "TU_TOKEN_AQUI":
            print("❌ Error: Configura tu token en config.json")
            sys.exit(1)

        print(f"🚀 Iniciando {self.config['branding']['bot_name']} (Versión Robusta)...")
        print(f"📢 Canal: {self.channel}")
        print(f"🔌 APIs disponibles: {sum(1 for api in self.apis.values() if api.get('enabled', False))} activas")

        # Crear aplicación
        self.application = Application.builder().token(self.token).build()

        # Añadir handlers
        for handler in self.get_handlers():
            self.application.add_handler(handler)

        # Ejecutar
        print("✅ Bot iniciado. Presiona Ctrl+C para detener.")
        
        # Configurar comandos antes de iniciar polling
        async def setup_bot():
            await self.set_commands(self.application.bot)
        
        # Configurar comandos inmediatamente
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(setup_bot())
        
        print("📱 Menú de comandos configurado en Telegram")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    bot = IADailyBotRobusto()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Deteniendo bot...")
        asyncio.run(bot.cleanup())
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
