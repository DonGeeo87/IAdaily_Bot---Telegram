#!/usr/bin/env python3
"""
🤖 IA Daily Bot - Bot de Telegram para publicación automática de contenido IA
Autor: Auto-generated
Canal: @IADaily_Bot
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

try:
    from telegram import Bot, Update
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError:
    print("❌ Instalando dependencias...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot, Update
    from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración de paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
LOGS_DIR = BASE_DIR / "logs"
POSTS_DIR = BASE_DIR / "posts"

# Asegurar directorios
LOGS_DIR.mkdir(exist_ok=True)
POSTS_DIR.mkdir(exist_ok=True)

# Configuración de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"bot_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class IADailyBot:
    """Bot principal de IA Daily"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = None
        self.application = None
        
    def load_config(self) -> dict:
        """Cargar configuración desde JSON"""
        if not CONFIG_FILE.exists():
            logger.error("❌ config.json no encontrado")
            sys.exit(1)
        
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        welcome = f"""
👋 ¡Hola! Soy **{self.config['branding']['bot_name']}**

{self.config['branding']['tagline']}

📌 **Comandos disponibles:**

🎯 **PRINCIPALES:**
/start - Iniciar el bot
/generar - Generar contenido de IA
/campana - Obtener campaña de promoción del día
/post - Crear post para redes sociales
/prompts - Recibir prompts de ChatGPT

📊 **INFO:**
/schedule - Ver horario de publicaciones
/status - Estado del bot (admins)
/help - Ayuda completa
/stats - Estadísticas del canal

🔧 **ADMIN:**
/admin - Panel de administrador
/config - Ver configuración

📢 Canal: {self.channel}

💡 *Escribe /help para ver todos los detalles*
        """
        await update.message.reply_text(welcome, parse_mode='HTML')
        logger.info(f"Usuario {update.effective_user.id} inició el bot")
    
    async def generar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /generar - Generar contenido de IA"""
        await update.message.reply_text(
            "🤖 Generando contenido de IA...\n\n"
            "Esto puede tomar unos segundos.",
            parse_mode='HTML'
        )
        
        try:
            # Ejecutar generador de contenido
            import subprocess
            result = subprocess.run(
                ['python', str(BASE_DIR / 'content_generator.py')],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR)
            )
            
            if result.returncode == 0:
                # Leer posts generados
                import os
                posts_dir = BASE_DIR / 'posts'
                today = datetime.now().strftime("%Y%m%d")
                
                mensaje = "✅ **Contenido generado:**\n\n"
                for post_type in ['herramienta', 'noticia', 'tip', 'recurso', 'prompt']:
                    filename = posts_dir / f"{today}_{post_type}.txt"
                    if filename.exists():
                        with open(filename, 'r', encoding='utf-8') as f:
                            content = f.read()[:500]  # Primeros 500 chars
                        mensaje += f"📄 **{post_type}:**\n`{content}...`\n\n"
                
                mensaje += "\n📁 Archivos completos en: `~/telegram-ia-bot/posts/`"
                
                await update.message.reply_text(mensaje, parse_mode='HTML')
            else:
                await update.message.reply_text(f"❌ Error al generar: {result.stderr}")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def campana(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /campana - Obtener campaña de promoción"""
        await update.message.reply_text(
            "🚀 Generando campaña de promoción...\n\n"
            "Te enviaré 4 posts listos para publicar hoy.",
            parse_mode='HTML'
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
                await update.message.reply_text(
                    "✅ **Campaña generada!**\n\n"
                    "Revisa tu Telegram para ver los posts completos.\n\n"
                    "📁 También disponibles en: `~/telegram-ia-bot/campaign/`",
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(f"❌ Error: {result.stderr}")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")
    
    async def post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /post - Crear post para redes"""
        if not context.args:
            await update.message.reply_text(
                "📝 **Crear Post para Redes**\n\n"
                "Uso: `/post [tema]`\n\n"
                "Ejemplos:\n"
                "`/post ChatGPT`\n"
                "`/post herramientas de productividad`\n"
                "`/post noticias de IA`\n\n"
                "Generaré un post listo para publicar.",
                parse_mode='HTML'
            )
            return
        
        tema = ' '.join(context.args)
        await update.message.reply_text(
            f"🤖 Creando post sobre: **{tema}**\n\n"
            "Esto tomará unos segundos...",
            parse_mode='HTML'
        )
        
        # Generar post simple
        post_content = f"""
🤖 **{tema.title()}**

La inteligencia artificial está transformando la forma en que trabajamos con {tema}.

💡 **Lo que necesitas saber:**
- Herramientas nuevas aparecen cada día
- Los prompts correctos hacen la diferencia
- La práctica constante es clave

📚 **Recursos recomendados:**
1. ChatGPT para redacción
2. Midjourney para imágenes
3. Notion AI para organización

👉 Únete a nuestro canal para más contenido:
t.me/IADailyChannel

#IA #InteligenciaArtificial #{tema.replace(' ', '')}
        """
        
        await update.message.reply_text(post_content, parse_mode='HTML')
    
    async def prompts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /prompts - Recibir prompts de ChatGPT"""
        prompts_list = [
            {
                "categoria": "Productividad",
                "prompt": "Actúa como un experto en productividad. Tengo estas tareas: [LISTA]. Priorízalas usando la matriz de Eisenhower y dime cuál hacer primero, cuál delegar, cuál programar y cuál eliminar."
            },
            {
                "categoria": "Aprendizaje",
                "prompt": "Explícame [TEMA] como si tuviera 10 años. Usa analogías simples y ejemplos cotidianos. Al final, hazme 3 preguntas para verificar mi comprensión."
            },
            {
                "categoria": "Redacción",
                "prompt": "Escribe un [TIPO DE TEXTO] para [AUDIENCIA]. El tono debe ser [TONO]. Incluye: introducción llamativa, 3 puntos principales, y un call-to-action claro."
            },
            {
                "categoria": "Código",
                "prompt": "Escribe una función en [LENGUAJE] que haga [X]. Incluye comentarios explicando cada parte, manejo de errores, y ejemplos de uso con diferentes inputs."
            },
            {
                "categoria": "Análisis",
                "prompt": "Analiza el siguiente texto y extrae: 1) Puntos clave 2) Argumentos principales 3) Posibles contraargumentos 4) Sesgos potenciales 5) Conclusión en 1 frase."
            }
        ]
        
        mensaje = "🎯 **Prompts de ChatGPT Listos para Usar**\n\n"
        
        for i, item in enumerate(prompts_list, 1):
            mensaje += f"**{i}. {item['categoria']}:**\n"
            mensaje += f"`{item['prompt']}`\n\n"
        
        mensaje += "\n💡 *Copia y pega en ChatGPT, reemplazando [X] con tu caso específico*"
        
        await update.message.reply_text(mensaje, parse_mode='HTML')
    
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats - Estadísticas"""
        await update.message.reply_text(
            "📊 **Estadísticas del Canal**\n\n"
            f"Canal: {self.channel}\n"
            "Estado: ✅ Activo\n\n"
            "📈 Para ver estadísticas detalladas:\n"
            "`python growth_tracker.py`\n\n"
            "El bot publica 4 veces al día automáticamente.",
            parse_mode='HTML'
        )
    
    async def admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /admin - Panel de administrador"""
        admin_panel = """
🔧 **Panel de Administrador**

📌 **Comandos rápidos:**

/generar - Generar contenido nuevo
/campana - Campaña de promoción
/post [tema] - Crear post personalizado
/prompts - Ver prompts de ChatGPT

📁 **Archivos importantes:**
- Config: `config.json`
- Posts: `posts/`
- Campañas: `campaign/`
- Logs: `logs/`

🚀 **Scripts útiles:**
- `python scheduler.py` - Auto-post
- `python campaign_manager.py` - Promoción
- `python content_generator.py` - Contenido
- `bash promote.sh` - Promoción completa
        """
        await update.message.reply_text(admin_panel, parse_mode='HTML')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Ayuda completa"""
        help_text = """
📚 **Ayuda Completa - IA Daily Bot**

🤖 **SOBRE ESTE BOT:**
Este bot automatiza la creación y promoción de contenido sobre Inteligencia Artificial.

📌 **COMANDOS PRINCIPALES:**

🎯 **Generación de Contenido:**
/start - Iniciar el bot
/generar - Crear contenido de IA automáticamente
/post [tema] - Crear post personalizado sobre un tema
/prompts - Recibir 5 prompts de ChatGPT listos

🚀 **Promoción:**
/campana - Obtener campaña de promoción del día (4 posts)

📊 **Información:**
/schedule - Ver horario de publicaciones
/stats - Estadísticas del canal
/status - Estado del bot (solo admins)
/admin - Panel de administrador
/help - Esta ayuda

💡 **EJEMPLOS DE USO:**

1. **Generar contenido diario:**
   `/generar`

2. **Obtener promoción del día:**
   `/campana`

3. **Crear post sobre un tema:**
   `/post ChatGPT`

4. **Recibir prompts útiles:**
   `/prompts`

📁 **UBICACIÓN DE ARCHIVOS:**
- Contenido: `~/telegram-ia-bot/posts/`
- Campañas: `~/telegram-ia-bot/campaign/`
- Logs: `~/telegram-ia-bot/logs/`

🔧 **COMANDOS DE TERMINAL:**
- `python scheduler.py` - Publicación automática
- `python campaign_manager.py` - Campañas
- `bash enviar_contenido.sh` - Enviar todo

¿Preguntas? Revisa el README.md para más detalles.
        """
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def schedule(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /schedule - Mostrar horario"""
        times = self.config["schedule"]["times"]
        schedule_msg = "⏰ **Horario de Publicaciones:**\n\n"
        
        emojis = ["🌅", "☀️", "🌆", "🌙"]
        for i, time in enumerate(times):
            emoji = emojis[i % len(emojis)]
            schedule_msg += f"{emoji} {time} - Publicación automática\n"
        
        schedule_msg += f"\n📊 Posts por día: {self.config['schedule']['posts_per_day']}"
        schedule_msg += f"\n🌐 Zona horaria: {self.config['schedule']['timezone']}"
        
        await update.message.reply_text(schedule_msg, parse_mode='HTML')
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - Estado del bot"""
        # Verificar si es admin
        if update.effective_user.id not in self.config["telegram"]["admin_users"]:
            await update.message.reply_text("⛔ Solo administradores pueden ver el estado")
            return
        
        status_msg = f"""
🤖 **Estado del Bot**

✅ Bot: Activo
📢 Canal: {self.channel}
⏰ Auto-post: {'✅ Activado' if self.config['features']['auto_post'] else '❌ Desactivado'}
📝 Logs: {'✅ Activados' if self.config['features']['log_activity'] else '❌ Desactivados'}
🔄 Reintentos: {self.config['features']['max_retries']} máx.

📁 Directorios:
- Logs: {LOGS_DIR}
- Posts: {POSTS_DIR}
        """
        await update.message.reply_text(status_msg, parse_mode='HTML')
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Ayuda"""
        help_text = """
📚 **Ayuda - IA Daily Bot**

🤖 **Sobre este bot:**
Este bot publica automáticamente contenido sobre Inteligencia Artificial en nuestro canal de Telegram.

📌 **Contenido que publicamos:**
- 🛠️ Nuevas herramientas de IA
- 📰 Noticias del mundo IA
- 💡 Tips y prompts útiles
- 📦 Recursos gratuitos

⏰ **Frecuencia:** 4 publicaciones diarias

🔧 **Comandos:**
/start - Iniciar
/schedule - Ver horario
/status - Estado (admins)
/help - Esta ayuda

¿Preguntas? Contacta al admin del canal.
        """
        await update.message.reply_text(help_text, parse_mode='HTML')
    
    async def publish_post(self, content: str, image_path: str = None):
        """Publicar un post en el canal"""
        try:
            if not self.bot:
                self.bot = Bot(token=self.token)
            
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img:
                    await self.bot.send_photo(
                        chat_id=self.channel,
                        photo=img,
                        caption=content,
                        parse_mode='HTML'
                    )
            else:
                await self.bot.send_message(
                    chat_id=self.channel,
                    text=content,
                    parse_mode='HTML'
                )
            
            logger.info("✅ Post publicado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al publicar: {e}")
            return False
    
    def get_bot_handlers(self):
        """Obtener handlers de comandos"""
        return [
            CommandHandler('start', self.start),
            CommandHandler('generar', self.generar),
            CommandHandler('campana', self.campana),
            CommandHandler('post', self.post),
            CommandHandler('prompts', self.prompts),
            CommandHandler('schedule', self.schedule),
            CommandHandler('status', self.status),
            CommandHandler('stats', self.stats),
            CommandHandler('admin', self.admin),
            CommandHandler('help', self.help_command),
        ]
    
    def run(self):
        """Ejecutar el bot"""
        if self.token == "TU_TOKEN_AQUI":
            print("❌ Error: Debes configurar tu token en config.json")
            print("📝 Sigue las instrucciones en README.md")
            sys.exit(1)
        
        print(f"🚀 Iniciando {self.config['branding']['bot_name']}...")
        print(f"📢 Canal: {self.channel}")
        print(f"⏰ Posts/día: {self.config['schedule']['posts_per_day']}")
        
        self.application = Application.builder().token(self.token).build()
        
        # Añadir handlers
        for handler in self.get_bot_handlers():
            self.application.add_handler(handler)
        
        # Iniciar polling
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Función principal"""
    bot = IADailyBot()
    bot.run()


if __name__ == '__main__':
    main()
