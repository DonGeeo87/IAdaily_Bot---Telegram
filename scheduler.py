#!/usr/bin/env python3
"""
⏰ Scheduler - Programador de publicaciones automáticas
Publica contenido en horarios configurados
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    import schedule
    import time
except ImportError:
    print("📦 Instalando schedule...")
    os.system("pip install schedule")
    import schedule
    import time

try:
    from telegram import Bot
except ImportError:
    print("📦 Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
LOGS_DIR = BASE_DIR / "logs"
POSTS_DIR = BASE_DIR / "posts"
SCHEDULED_POSTS_FILE = POSTS_DIR / "scheduled.json"

# Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class Scheduler:
    """Programador de publicaciones automáticas"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = Bot(token=self.token)
        self.posts_done_today = 0
        
    def load_config(self) -> dict:
        """Cargar configuración"""
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_scheduled_posts(self) -> list:
        """Cargar posts programados desde archivo"""
        if SCHEDULED_POSTS_FILE.exists():
            with open(SCHEDULED_POSTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_scheduled_posts(self, posts: list):
        """Guardar posts programados"""
        with open(SCHEDULED_POSTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
    
    def get_content_for_time(self, current_time: datetime) -> Optional[dict]:
        """Obtener contenido apropiado para la hora actual"""
        hour = current_time.hour
        
        # Contenido según la hora
        content_types = {
            (7, 9): {
                "type": "herramientas",
                "template": self.get_herramienta_template(),
                "emoji": "🌅"
            },
            (11, 13): {
                "type": "noticias", 
                "template": self.get_noticia_template(),
                "emoji": "☀️"
            },
            (15, 17): {
                "type": "tips",
                "template": self.get_tip_template(),
                "emoji": "🌆"
            },
            (19, 21): {
                "type": "recursos",
                "template": self.get_recurso_template(),
                "emoji": "🌙"
            }
        }
        
        for (start, end), content in content_types.items():
            if start <= hour <= end:
                return content
        
        return None
    
    def get_herramienta_template(self) -> str:
        """Template para herramientas IA"""
        templates = [
            """
🛠️ **Herramienta IA del Día**

📌 **{name}**

{description}

🔗 Enlace: {url}

💡 *Ideal para:* {use_case}

{footer}
            """,
            """
🚀 **Nueva Herramienta de IA**

Nombre: **{name}**

{description}

👉 Pruébala: {url}

{footer}
            """
        ]
        return templates[0]
    
    def get_noticia_template(self) -> str:
        """Template para noticias"""
        return """
📰 **Noticia IA**

{title}

{summary}

📖 Leer más: {url}

{footer}
        """
    
    def get_tip_template(self) -> str:
        """Template para tips"""
        return """
💡 **Tip IA del Día**

{tip}

📝 **Ejemplo:**
{example}

{footer}
        """
    
    def get_recurso_template(self) -> str:
        """Template para recursos"""
        return """
📦 **Recurso Gratuito**

📚 **{name}**

{description}

🎁 **Gratis por tiempo limitado**

👉 Descarga: {url}

{footer}
        """
    
    def format_post(self, content_type: dict, data: dict) -> str:
        """Formatear post con template"""
        template = content_type["template"]
        
        # Añadir emoji y footer
        data["emoji"] = content_type.get("emoji", "🤖")
        data["footer"] = self.config["branding"]["footer"]
        
        return template.format(**data)
    
    async def publish(self, content: str, image_path: str = None):
        """Publicar contenido"""
        try:
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
            
            logger.info("✅ Post publicado")
            self.posts_done_today += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al publicar: {e}")
            return False
    
    async def auto_post(self):
        """Función automática de publicación"""
        now = datetime.now()
        content_info = self.get_content_for_time(now)
        
        if not content_info:
            logger.info("⏭️ No hay contenido programado para esta hora")
            return
        
        # Generar contenido de ejemplo (puedes conectar a APIs reales)
        sample_data = {
            "name": "ChatGPT-4o",
            "description": "Nueva versión multimodal de OpenAI con capacidades mejoradas de visión y voz.",
            "url": "https://openai.com",
            "use_case": "Creación de contenido multimedia interactivo",
            "title": "OpenAI anuncia GPT-4o",
            "summary": "La nueva versión es más rápida y tiene mejores capacidades de razonamiento.",
            "tip": "Usa prompts específicos con contexto para obtener mejores resultados.",
            "example": "En lugar de 'escribe un email', usa 'escribe un email profesional para solicitar una reunión con un cliente potencial en el sector tech'"
        }
        
        post_content = self.format_post(content_info, sample_data)
        
        # Publicar
        await self.publish(post_content)
        
        # Guardar en historial
        scheduled = self.load_scheduled_posts()
        scheduled.append({
            "date": now.isoformat(),
            "type": content_info["type"],
            "status": "published"
        })
        self.save_scheduled_posts(scheduled)
    
    def setup_schedule(self):
        """Configurar horarios de publicación"""
        times = self.config["schedule"]["times"]
        
        for time_str in times:
            schedule.every().day.at(time_str).do(
                lambda: self.run_async(self.auto_post())
            )
            logger.info(f"⏰ Programado post a las {time_str}")
    
    def run_async(self, coro):
        """Ejecutar función async"""
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    
    def run(self):
        """Ejecutar scheduler"""
        if self.token == "TU_TOKEN_AQUI":
            print("❌ Configura tu token en config.json primero")
            sys.exit(1)
        
        print(f"🚀 Scheduler iniciado - {self.config['branding']['bot_name']}")
        print(f"📢 Canal: {self.channel}")
        print(f"⏰ Horarios: {', '.join(self.config['schedule']['times'])}")
        print("📌 Presiona Ctrl+C para detener\n")
        
        self.setup_schedule()
        
        # Loop principal
        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    scheduler = Scheduler()
    scheduler.run()


if __name__ == '__main__':
    main()
