#!/usr/bin/env python3
"""
⏰ Master Scheduler - Programador maestro de TODAS las actividades
Integra: posts, engagement, welcome, y eventos especiales
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path

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
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"scheduler_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MasterScheduler:
    """Programador maestro de todas las actividades"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = Bot(token=self.token)
        
    def load_config(self) -> dict:
        """Cargar configuración con soporte para variables de entorno"""
        try:
            from config_loader import load_config_with_env, validate_config
            config = load_config_with_env(str(CONFIG_FILE))
            valid, msg = validate_config(config)
            if not valid:
                logger.error(f"❌ Configuración inválida:\n{msg}")
                sys.exit(1)
            logger.info("✅ Configuración cargada (archivo + variables de entorno)")
            return config
        except ImportError:
            logger.warning("config_loader.py no encontrado, usando config.json directamente")
        
        # Fallback a config.json tradicional
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def post_content(self, post_type: str):
        """Publicar contenido automático"""
        try:
            # Leer posts generados
            today = datetime.now().strftime("%Y%m%d")
            posts_dir = BASE_DIR / "posts"
            post_file = posts_dir / f"{today}_{post_type}.txt"
            
            if not post_file.exists():
                # Generar contenido si no existe
                logger.info(f"Generando contenido: {post_type}")
                os.system(f"cd {BASE_DIR} && python content_generator.py > /dev/null 2>&1")
            
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            await self.bot.send_message(
                chat_id=self.channel,
                text=content,
                parse_mode='HTML'
            )
            
            logger.info(f"✅ Publicado: {post_type}")
            
        except Exception as e:
            logger.error(f"❌ Error al publicar {post_type}: {e}")
    
    async def run_poll(self):
        """Publicar encuesta diaria"""
        try:
            from engagement_bot import EngagementBot
            engagement = EngagementBot()
            await engagement.post_daily_poll(None)
        except Exception as e:
            logger.error(f"❌ Error con encuesta: {e}")
    
    async def run_quiz(self):
        """Publicar quiz semanal"""
        try:
            from engagement_bot import EngagementBot
            engagement = EngagementBot()
            await engagement.post_weekly_quiz(None)
        except Exception as e:
            logger.error(f"❌ Error con quiz: {e}")
    
    async def run_challenge(self):
        """Publicar desafío diario"""
        try:
            from engagement_bot import EngagementBot
            engagement = EngagementBot()
            await engagement.post_daily_challenge(None)
        except Exception as e:
            logger.error(f"❌ Error con desafío: {e}")
    
    async def run_question(self):
        """Publicar pregunta de engagement"""
        try:
            from engagement_bot import EngagementBot
            engagement = EngagementBot()
            await engagement.post_engagement_question(None)
        except Exception as e:
            logger.error(f"❌ Error con pregunta: {e}")
    
    def run_async(self, coro):
        """Ejecutar función async"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    
    def setup_schedule(self):
        """Configurar todos los horarios"""
        logger.info("📅 Configurando horarios de actividades...")
        
        # Posts de contenido (4 veces al día)
        schedule.every().day.at("08:00").do(lambda: self.run_async(self.post_content("herramienta")))
        schedule.every().day.at("12:00").do(lambda: self.run_async(self.post_content("noticia")))
        schedule.every().day.at("16:00").do(lambda: self.run_async(self.post_content("tip")))
        schedule.every().day.at("20:00").do(lambda: self.run_async(self.post_content("recurso")))
        
        # Engagement
        schedule.every().day.at("10:00").do(lambda: self.run_async(self.run_challenge()))  # Desafío
        schedule.every().day.at("14:00").do(lambda: self.run_async(self.run_poll()))  # Encuesta
        schedule.every().day.at("16:30").do(lambda: self.run_async(self.run_question()))  # Pregunta
        schedule.every().friday.at("18:00").do(lambda: self.run_async(self.run_quiz()))  # Quiz semanal
        
        logger.info("✅ Horarios configurados:")
        logger.info("   08:00 - Herramienta IA")
        logger.info("   10:00 - Desafío del día")
        logger.info("   12:00 - Noticia IA")
        logger.info("   14:00 - Encuesta")
        logger.info("   16:00 - Tip/Prompt")
        logger.info("   16:30 - Pregunta engagement")
        logger.info("   20:00 - Recurso")
        logger.info("   Viernes 18:00 - Quiz semanal")
    
    def run(self):
        """Ejecutar scheduler"""
        print("=" * 60)
        print("⏰ MASTER SCHEDULER - IA Daily")
        print("=" * 60)
        print()
        print(f"📢 Canal: {self.channel}")
        print(f"🚀 Iniciando scheduler...")
        print()
        
        self.setup_schedule()
        
        print("\n✅ Scheduler activo. Presiona Ctrl+C para detener.\n")
        
        # Loop principal
        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    scheduler = MasterScheduler()
    
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("\n👋 Deteniendo scheduler...")
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")


if __name__ == '__main__':
    main()
