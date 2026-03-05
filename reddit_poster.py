#!/usr/bin/env python3
"""
🤖 Reddit Auto-Poster para IA Daily
Publica automáticamente en subreddits de IA
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

try:
    import praw
except ImportError:
    print("📦 Instalando PRAW (Reddit API)...")
    os.system("pip install praw")
    import praw

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "reddit_config.json"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"reddit_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RedditAutoPoster:
    """Publicador automático en Reddit"""
    
    def __init__(self):
        self.config = self.load_config()
        self.reddit = self.connect()
        
    def load_config(self) -> dict:
        """Cargar configuración de Reddit"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Config por defecto
        return {
            "credentials": {
                "client_id": "TU_CLIENT_ID",
                "client_secret": "TU_CLIENT_SECRET",
                "username": "TU_USUARIO",
                "password": "TU_PASSWORD",
                "user_agent": "IA Daily Bot v1.0 by /u/TU_USUARIO"
            },
            "subreddits": [
                {"name": "InteligenciaArtificial", "min_karma": 0},
                {"name": "IA", "min_karma": 0},
                {"name": "ChatGPT", "min_karma": 100},
                {"name": "artificial", "min_karma": 500},
                {"name": "MachineLearning", "min_karma": 1000},
                {"name": "technology", "min_karma": 500},
                {"name": "technews", "min_karma": 200},
                {"name": "singularity", "min_karma": 300}
            ],
            "posting": {
                "posts_per_day": 3,
                "delay_hours": 4,
                "include_channel_link": True
            }
        }
    
    def connect(self):
        """Conectar a Reddit"""
        try:
            reddit = praw.Reddit(
                client_id=self.config["credentials"]["client_id"],
                client_secret=self.config["credentials"]["client_secret"],
                username=self.config["credentials"]["username"],
                password=self.config["credentials"]["password"],
                user_agent=self.config["credentials"]["user_agent"]
            )
            
            # Verificar conexión
            logger.info(f"✅ Conectado como /u/{reddit.user.me()}")
            return reddit
            
        except Exception as e:
            logger.error(f"❌ Error de conexión: {e}")
            return None
    
    def get_submission_templates(self) -> list:
        """Plantillas de submissions"""
        return [
            {
                "title": "🤖 Herramienta IA del Día: {name}",
                "content": """
## {name}

{description}

🔗 **Enlace:** {url}

💡 **Casos de uso:**
{use_cases}

---

*Más herramientas diarias en nuestro canal de Telegram:* t.me/IADailyChannel

*Post automático de IA Daily Bot*
""",
                "flair": "Herramienta"
            },
            {
                "title": "📰 Noticia IA: {title}",
                "content": """
## {title}

{summary}

📖 **Fuente:** {url}

---

*Seguimiento diario de noticias de IA en:* t.me/IADailyChannel
""",
                "flair": "Noticia"
            },
            {
                "title": "💡 Tip de IA: {tip_title}",
                "content": """
## {tip_title}

{tip_content}

**Ejemplo:**
{example}

---

*Tips diarios en nuestro Telegram:* t.me/IADailyChannel
""",
                "flair": "Tutorial"
            },
            {
                "title": "📦 Recurso Gratuito: {name}",
                "content": """
## {name}

{description}

🎁 **100% Gratis**

👉 **Acceso:** {url}

---

*Más recursos en:* t.me/IADailyChannel
""",
                "flair": "Recurso"
            }
        ]
    
    def get_content_from_telegram(self) -> list:
        """Obtener contenido de los posts de Telegram"""
        posts_dir = BASE_DIR / "posts"
        content = []
        
        if not posts_dir.exists():
            return content
        
        # Leer últimos posts
        post_files = sorted(posts_dir.glob("*.txt"), reverse=True)[:5]
        
        for post_file in post_files:
            with open(post_file, 'r', encoding='utf-8') as f:
                post_content = f.read()
            
            # Determinar tipo
            if "herramienta" in post_file.name.lower():
                post_type = "herramienta"
            elif "noticia" in post_file.name.lower():
                post_type = "noticia"
            elif "tip" in post_file.name.lower():
                post_type = "tip"
            elif "recurso" in post_file.name.lower():
                post_type = "recurso"
            else:
                post_type = "general"
            
            content.append({
                "type": post_type,
                "content": post_content,
                "file": post_file.name
            })
        
        return content
    
    def parse_post_for_reddit(self, post_content: str, post_type: str) -> dict:
        """Parsear post de Telegram para formato Reddit"""
        
        # Datos por defecto
        data = {
            "name": "Herramienta de IA",
            "description": "Herramienta útil para productividad con IA",
            "url": "https://t.me/IADailyChannel",
            "use_cases": "- Productividad\n- Automatización",
            "title": "Novedad de IA",
            "summary": "Información interesante sobre IA",
            "tip_title": "Tip útil",
            "tip_content": "Consejo para mejorar con IA",
            "example": "Ejemplo práctico"
        }
        
        # Parsear contenido (simple)
        lines = post_content.split('\n')
        for line in lines:
            if '📌' in line or '**' in line:
                data["name"] = line.replace('📌', '').replace('**', '').strip()
            elif '🔗' in line and 'Enlace' in line:
                data["url"] = line.split(':')[-1].strip()
            elif '💡' in line and 'Ideal' in line:
                data["use_cases"] = line.replace('💡', '').replace('*Ideal para:*', '').strip()
        
        return data
    
    def submit_to_subreddit(self, subreddit_name: str, title: str, content: str, flair: str = None):
        """Publicar en un subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Submit texto
            submission = subreddit.submit(title, selftext=content)
            
            logger.info(f"✅ Publicado en r/{subreddit_name}: {title[:50]}...")
            logger.info(f"   URL: {submission.shortlink}")
            
            # Intentar añadir flair
            if flair:
                try:
                    flair_templates = subreddit.flair.link_flair_templates
                    for template in flair_templates:
                        if flair.lower() in template['text'].lower():
                            submission.flair.select(template['id'])
                            logger.info(f"   Flair añadida: {flair}")
                            break
                except Exception as e:
                    logger.warning(f"   No se pudo añadir flair: {e}")
            
            return submission.shortlink
            
        except Exception as e:
            logger.error(f"❌ Error en r/{subreddit_name}: {e}")
            return None
    
    def check_karma(self) -> dict:
        """Verificar karma del usuario"""
        try:
            user = self.reddit.redditor(self.config["credentials"]["username"])
            
            karma = {
                "post_karma": user.link_karma,
                "comment_karma": user.comment_karma,
                "total_karma": user.link_karma + user.comment_karma,
                "account_age_days": (datetime.now().timestamp() - user.created_utc) / 86400
            }
            
            logger.info(f"📊 Karma: {karma['total_karma']} (Post: {karma['post_karma']}, Comment: {karma['comment_karma']})")
            logger.info(f"   Edad de cuenta: {karma['account_age_days']:.0f} días")
            
            return karma
            
        except Exception as e:
            logger.error(f"❌ Error al verificar karma: {e}")
            return {}
    
    def get_eligible_subreddits(self, karma: dict) -> list:
        """Obtener subreddits donde se puede publicar según karma"""
        eligible = []
        
        for subreddit in self.config["subreddits"]:
            min_karma = subreddit.get("min_karma", 0)
            if karma.get("total_karma", 0) >= min_karma:
                eligible.append(subreddit["name"])
            else:
                logger.info(f"⏭️  r/{subreddit['name']} requiere {min_karma} karma (tienes {karma.get('total_karma', 0)})")
        
        return eligible
    
    def post_to_reddit(self):
        """Publicar contenido en Reddit"""
        if not self.reddit:
            logger.error("❌ No hay conexión a Reddit")
            return False
        
        # Verificar karma
        karma = self.check_karma()
        
        # Obtener subreddits elegibles
        eligible = self.get_eligible_subreddits(karma)
        
        if not eligible:
            logger.error("❌ No hay subreddits elegibles. Necesitas más karma.")
            return False
        
        logger.info(f"📋 Subreddits disponibles: {len(eligible)}")
        
        # Obtener contenido
        telegram_posts = self.get_content_from_telegram()
        
        if not telegram_posts:
            logger.error("❌ No hay contenido de Telegram")
            return False
        
        # Obtener plantillas
        templates = self.get_submission_templates()
        
        # Publicar
        posted = 0
        max_posts = self.config["posting"]["posts_per_day"]
        
        for post in telegram_posts[:max_posts]:
            # Parsear contenido
            data = self.parse_post_for_reddit(post["content"], post["type"])
            
            # Seleccionar template según tipo
            template = next((t for t in templates if t["flair"].lower() in post["type"].lower()), templates[0])
            
            # Formatear título y contenido
            title = template["title"].format(**data)
            content = template["content"].format(**data)
            
            # Publicar en subreddits elegibles (máximo 3 por post)
            for subreddit in eligible[:3]:
                shortlink = self.submit_to_subreddit(
                    subreddit,
                    title,
                    content,
                    template["flair"]
                )
                
                if shortlink:
                    posted += 1
            
            # Delay entre posts
            import time
            time.sleep(5)
        
        logger.info(f"\n✅ {posted} publicaciones realizadas")
        return posted > 0
    
    def save_config_template(self):
        """Guardar plantilla de configuración"""
        if not CONFIG_FILE.exists():
            config = self.load_config()
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Plantilla guardada en: {CONFIG_FILE}")
            return True
        return False


def main():
    print("=" * 50)
    print("🤖 Reddit Auto-Poster para IA Daily")
    print("=" * 50)
    print()
    
    poster = RedditAutoPoster()
    
    # Verificar si es primera vez
    if not CONFIG_FILE.exists():
        print("⚠️  Primera ejecución!")
        print()
        print("📝 Necesitas configurar tus credenciales de Reddit API")
        print()
        print("Pasos:")
        print("1. Ve a https://www.reddit.com/prefs/apps")
        print("2. Crea una aplicación (tipo 'script')")
        print("3. Copia client_id y client_secret")
        print("4. Edita reddit_config.json con tus datos")
        print()
        
        poster.save_config_template()
        print(f"✅ Archivo de configuración creado: {CONFIG_FILE}")
        print()
        print("Luego ejecuta este script nuevamente")
        return
    
    # Verificar conexión
    if not poster.reddit:
        print("❌ Error de conexión. Verifica tus credenciales")
        return
    
    # Publicar
    success = poster.post_to_reddit()
    
    if success:
        print("\n✅ ¡Publicaciones completadas!")
    else:
        print("\n⚠️  No se pudo publicar. Revisa los logs")


if __name__ == '__main__':
    main()
