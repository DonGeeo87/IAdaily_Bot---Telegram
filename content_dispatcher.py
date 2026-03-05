#!/usr/bin/env python3
"""
📤 Content Dispatcher - Envía contenido listo para publicar
Te envía los posts formateados para cada red social directamente a Telegram
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

try:
    from telegram import Bot
except ImportError:
    print("Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
POSTS_DIR = BASE_DIR / "posts"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"dispatcher_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ContentDispatcher:
    """Envía contenido formateado para cada red social"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.bot = Bot(token=self.token)
        self.admin_chat_id = None  # Se obtiene automáticamente
        
    def load_config(self) -> dict:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def get_my_chat_id(self):
        """Obtener tu chat ID automáticamente"""
        updates = await self.bot.get_updates(offset=-1)
        if updates:
            return updates[0].effective_user.id
        # Si no hay updates, usar el admin_users si existe
        admins = self.config["telegram"].get("admin_users", [])
        if admins:
            return admins[0]
        return None
    
    def format_for_reddit(self, content: str, post_type: str) -> str:
        """Formatear para Reddit"""
        # Extraer datos del contenido
        data = self.extract_data_from_content(content)
        data["content"] = content  # Añadir contenido completo
        
        templates = {
            "herramienta": f"""
📢 **LISTO PARA REDDIT**

**Subreddits sugeridos:**
• r/InteligenciaArtificial
• r/IA
• r/ChatGPT

---

**TÍTULO:**
🤖 Herramienta IA del Día: {data['name']}

**CONTENIDO:**
{content}

---

**Flair recomendado:** Herramienta / Resource
**No olvides:** Responder comentarios para más engagement
            """,
            "noticia": f"""
📢 **LISTO PARA REDDIT**

**Subreddits sugeridos:**
• r/technology
• r/technews
• r/singularity

---

**TÍTULO:**
📰 Noticia IA: {data.get('title', 'Novedad de IA')}

**CONTENIDO:**
{content}

---

**Flair recomendado:** News / Discussion
            """,
            "tip": f"""
📢 **LISTO PARA REDDIT**

**Subreddits sugeridos:**
• r/ChatGPT
• r/InteligenciaArtificial
• r/productivity

---

**TÍTULO:**
💡 Tip: Cómo mejorar tus prompts de IA

**CONTENIDO:**
{content}

---

**Flair recomendado:** Tutorial / Tips & Tricks
            """,
            "recurso": f"""
📢 **LISTO PARA REDDIT**

**Subreddits sugeridos:**
• r/InteligenciaArtificial
• r/Freebies
• r/ChatGPT

---

**TÍTULO:**
📦 Recurso Gratuito: {data['name']}

**CONTENIDO:**
{content}

---

**Flair recomendado:** Free Resource / Tutorial
            """
        }
        
        template = templates.get(post_type, templates["herramienta"])
        return template
    
    def format_for_twitter(self, content: str) -> str:
        """Formatear para Twitter/X (280 chars)"""
        hashtags = "#IA #InteligenciaArtificial #AI #TechNews #AIEspañol"
        
        # Extraer parte importante
        lines = content.split('\n')
        important = [l for l in lines if l.strip() and not l.startswith('📢')][0:3]
        summary = ' '.join(important)[:200]
        
        return f"""
📢 **LISTO PARA TWITTER**

**Tweet:**
{summary}

👉 Más en: t.me/IADailyChannel

{hashtags}

---

**Hilo sugerido:**
1/ Tweet principal (arriba)
2/ Responder con más detalles
3/ Responder con enlace al canal
            """
    
    def format_for_linkedin(self, content: str) -> str:
        """Formatear para LinkedIn"""
        return f"""
📢 **LISTO PARA LINKEDIN**

**Post profesional:**

🤖 IA Daily Channel

La inteligencia artificial está transformando la forma en que trabajamos.

{content[:500]}

...

Síguenos para más contenido sobre Inteligencia Artificial.

🔗 https://t.me/IADailyChannel

#InteligenciaArtificial #IA #Tecnología #Innovación #AI

---

**Tip:** Añade una imagen relacionada para +200% engagement
            """
    
    def format_for_instagram(self, content: str) -> str:
        """Formatear para Instagram"""
        hashtags = """
#ia #inteligenciaartificial #ai #artificialintelligence 
#tecnologia #innovation #tech #machinelearning #deeplearning 
#chatgpt #openai #programming #coding #technews #futuro 
#automatizacion #aiart #midjourney #promptengineering
"""
        return f"""
📢 **LISTO PARA INSTAGRAM**

**Caption:**

🤖 ¿Listo para dominar la IA?

{content[:300]}

...

👉 Link en bio: t.me/IADailyChannel

{hashtags}

---

**Story sugerida:**
• Crea un diseño en Canva con el título
• Añade sticker de "Link" hacia t.me/IADailyChannel
• Publica 1 hora después del post principal
            """
    
    def format_for_tiktok(self, content: str) -> str:
        """Formatear para TikTok"""
        return f"""
📢 **LISTO PARA TIKTOK**

**Guion (30 segundos):**

🎬 [0-3s] HOOK:
"¿Sabías que esta IA puede hacer [X] en segundos?"

🎬 [3-15s] DEMO:
Muestra la herramienta/caso de uso en pantalla

🎬 [15-25s] VALOR:
"Esto te ahorra X horas de trabajo"

🎬 [25-30s] CTA:
"Síguenos en Telegram para más → Link en bio"

---

**Descripción del video:**
🤖 Herramienta IA que debes conocer
#ia #inteligenciaartificial #ai #tech #herramientas #productividad

**Contenido base:**
{content[:200]}
            """
    
    def format_for_facebook(self, content: str) -> str:
        """Formatear para Facebook"""
        return f"""
📢 **LISTO PARA FACEBOOK**

**Post para grupos y perfil:**

🤖 IA Daily Channel

¿Te interesa la Inteligencia Artificial pero no tienes tiempo de buscar información?

{content[:400]}

...

Nosotros lo hacemos por ti. 4 posts diarios con lo más importante.

¡Únete gratis! 👇
https://t.me/IADailyChannel

---

**Grupos sugeridos:**
• Inteligencia Artificial en Español
• IA y Machine Learning
• ChatGPT & AI Tools
• Tecnología y Innovación
            """
    
    def extract_data_from_content(self, content: str) -> dict:
        """Extraer datos del contenido para templates"""
        data = {
            "name": "Herramienta de IA",
            "description": content[:200],
            "title": "Novedad de IA",
            "url": "https://t.me/IADailyChannel"
        }
        
        # Intentar extraer nombre
        for line in content.split('\n'):
            if '📌' in line:
                data["name"] = line.replace('📌', '').replace('**', '').strip()
            elif '🔗' in line:
                data["url"] = line.split(':')[-1].strip()
        
        return data
    
    async def send_to_user(self, message: str):
        """Enviar mensaje al usuario"""
        chat_id = await self.get_my_chat_id()
        
        if not chat_id:
            logger.error("❌ No se pudo obtener tu chat ID")
            logger.error("   Envía /start al bot primero")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Enviado a chat_id: {chat_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error al enviar: {e}")
            return False
    
    async def dispatch_all(self):
        """Generar y enviar todo el contenido"""
        print("=" * 50)
        print("📤 Content Dispatcher - IA Daily")
        print("=" * 50)
        
        # Obtener posts generados
        if not POSTS_DIR.exists():
            print("❌ No hay posts generados")
            print("   Ejecuta: python content_generator.py")
            return
        
        post_files = sorted(POSTS_DIR.glob("*.txt"), reverse=True)[:5]
        
        if not post_files:
            print("❌ No hay archivos de posts")
            return
        
        print(f"\n📦 Procesando {len(post_files)} posts...")
        
        # Enviar cada post
        for post_file in post_files:
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determinar tipo
            post_type = "herramienta"
            for t in ["herramienta", "noticia", "tip", "recurso", "prompt"]:
                if t in post_file.name.lower():
                    post_type = t
                    break
            
            print(f"\n📄 Procesando: {post_file.name} ({post_type})")
            
            # Formatear para cada plataforma
            formatted = {
                "Reddit": self.format_for_reddit(content, post_type),
                "Twitter": self.format_for_twitter(content),
                "LinkedIn": self.format_for_linkedin(content),
                "Instagram": self.format_for_instagram(content),
                "TikTok": self.format_for_tiktok(content),
                "Facebook": self.format_for_facebook(content)
            }
            
            # Enviar al usuario
            for platform, text in formatted.items():
                message = f"""
╔═══════════════════════════════════╗
   📱 **{platform}**
╚═══════════════════════════════════╗

{text}

---

💡 *Copia y pega en {platform}*
                """
                await self.send_to_user(message)
                await asyncio.sleep(0.5)
        
        print("\n✅ ¡Todo enviado!")
        print("\n📱 Revisa Telegram para ver el contenido formateado")
        print("   Solo copia y pega en cada red social")


async def main():
    dispatcher = ContentDispatcher()
    await dispatcher.dispatch_all()


if __name__ == '__main__':
    asyncio.run(main())
