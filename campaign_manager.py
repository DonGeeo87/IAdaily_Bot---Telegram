#!/usr/bin/env python3
"""
🚀 Campaign Manager - Campaña de promoción estratégica para @IADailyChannel
Genera 4 posts diarios DE PROMOCIÓN con links incluidos
"""

import os
import sys
import json
import asyncio
import random
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
CAMPAIGN_DIR = BASE_DIR / "campaign"
LOGS_DIR = BASE_DIR / "logs"
CAMPAIGN_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"campaign_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CampaignManager:
    """Genera campaña de promoción estratégica"""

    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.bot = Bot(token=self.token)
        self.channel = "https://t.me/IADailyChannel"
        # Obtener chat_id del owner o admin
        self.admin_chat_id = self.config.get("telegram", {}).get("owner_chat_id")
        if not self.admin_chat_id:
            admin_users = self.config.get("telegram", {}).get("admin_users", [])
            if admin_users:
                self.admin_chat_id = admin_users[0]
        
        # Plataformas SEGURA para compartir Telegram
        self.safe_platforms = {
            "twitter": {
                "name": "Twitter/X",
                "safe": True,
                "link_policy": "Permite links de Telegram",
                "best_times": ["09:00", "13:00", "18:00", "21:00"]
            },
            "reddit": {
                "name": "Reddit",
                "safe": True,
                "link_policy": "Permite en mayoría de subreddits (revisar reglas)",
                "best_times": ["10:00", "15:00", "20:00"]
            },
            "linkedin": {
                "name": "LinkedIn",
                "safe": True,
                "link_policy": "Permite links en posts y perfil",
                "best_times": ["08:00", "12:00", "17:00"]
            },
            "pinterest": {
                "name": "Pinterest",
                "safe": True,
                "link_policy": "Permite en pines y perfil",
                "best_times": ["11:00", "16:00", "20:00"]
            },
            "youtube": {
                "name": "YouTube",
                "safe": True,
                "link_policy": "Permite en descripción y comunidad",
                "best_times": ["12:00", "18:00"]
            },
            "tiktok": {
                "name": "TikTok",
                "safe": "bio",
                "link_policy": "Solo en bio (10k seguidores) o TikTok Business",
                "best_times": ["11:00", "16:00", "21:00"]
            },
            "instagram": {
                "name": "Instagram",
                "safe": "bio_stories",
                "link_policy": "Solo en bio y stories (no en posts)",
                "best_times": ["10:00", "15:00", "20:00"]
            },
            "facebook_groups": {
                "name": "Facebook Groups",
                "safe": "varies",
                "link_policy": "Depende del grupo (algunos borran)",
                "best_times": ["09:00", "14:00", "19:00"]
            }
        }
        
        # Subreddits que permiten Telegram (verificado)
        self.telegram_friendly_subreddits = [
            {"name": "TelegramChannels", "min_karma": 0, "description": "Canales de Telegram"},
            {"name": "TelegramGroups", "min_karma": 0, "description": "Grupos de Telegram"},
            {"name": "telegram", "min_karma": 10, "description": "Comunidad Telegram"},
            {"name": "InteligenciaArtificial", "min_karma": 0, "description": "IA en español"},
            {"name": "IA", "min_karma": 0, "description": "Inteligencia Artificial"},
            {"name": "ChatGPT", "min_karma": 50, "description": "ChatGPT y prompts"},
            {"name": "Freebies", "min_karma": 100, "description": "Recursos gratuitos"},
            {"name": "InternetIsBeautiful", "min_karma": 500, "description": "Sitios web útiles"},
            {"name": "Productivity", "min_karma": 100, "description": "Productividad"},
            {"name": "ArtificialInteligence", "min_karma": 50, "description": "Noticias de IA"}
        ]
        
    def load_config(self) -> dict:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def get_my_chat_id(self):
        """Obtener tu chat ID"""
        updates = await self.bot.get_updates(offset=-1)
        if updates and updates[0].effective_user:
            return updates[0].effective_user.id
        return None
    
    def get_promotion_posts_day_1(self) -> list:
        """Día 1: Presentación del canal"""
        return [
            {
                "platform": "reddit",
                "title": "🤖 Creé un canal que resume lo mejor de IA en 4 posts diarios",
                "content": f"""
Hola r/InteligenciaArtificial!

Después de meses de seguir el mundo de la IA, me cansé de:
- Noticias dispersas en 20 sitios diferentes
- Herramientas que nunca probaba por falta de tiempo
- Prompts que nunca guardaba

Así que creé **@IADailyChannel** - un canal que publica 4 veces al día:

🌅 **08:00** - Herramienta nueva del día
☀️ **12:00** - Noticia importante de IA
🌆 **16:00** - Tip o prompt útil
🌙 **20:00** - Recurso gratuito (curso, template, etc.)

**¿Por qué Telegram?**
- Sin algoritmos que escondan el contenido
- Notificaciones push reales
- Acceso rápido desde cualquier dispositivo

👉 **Únete gratis:** {self.channel}

Llevo 2 semanas probándolo y ya tengo herramientas que uso diariamente. 
El de hoy sobre [herramienta específica] me ahorró 3 horas de trabajo.

¿Qué opinan? ¿Alguien más usa Telegram para curar contenido de valor?

*PD: Cero spam, solo contenido que yo mismo uso.*
""",
                "subreddits": ["InteligenciaArtificial", "IA", "telegram"]
            },
            {
                "platform": "twitter",
                "content": f"""
🧵 Hilo: Las 5 herramientas de IA que uso TODOS los días

1/ [Herramienta 1] - Para escribir emails 10x más rápido
2/ [Herramienta 2] - Genera imágenes en segundos
3/ [Herramienta 3] - Resume artículos largos
4/ [Herramienta 4] - Crea presentaciones automáticas
5/ [Herramienta 5] - Transcribe reuniones

¿Quieres más herramientas como estas?

Las comparto diariamente en mi canal de Telegram:
👉 {self.channel}

(4 posts/día, cero spam, solo lo que uso)

#IA #InteligenciaArtificial #Productividad #AI
""",
                "thread_count": 6
            },
            {
                "platform": "linkedin",
                "content": f"""
🤖 La IA no te va a reemplazar. Pero alguien que usa IA sí.

Después de probar 50+ herramientas de IA en los últimos 6 meses, llegué a una conclusión:

El 90% son ruido.

Pero el 10% restante... ese 10% es oro puro.

Y es ese 10% el que comparto diariamente en mi canal de Telegram: @IADailyChannel

📍 ¿Qué encontrarás?
• Herramientas que realmente funcionan (las he probado)
• Noticias que impactan tu trabajo (no clickbait)
• Prompts listos para copiar y usar
• Recursos 100% gratuitos

📍 ¿Por qué Telegram?
• Contenido que llega SIEMPRE (sin algoritmos)
• Acceso rápido desde cualquier dispositivo
• Cero distracciones

👉 Únete gratis: {self.channel}

Actualmente publico 4 veces al día. 
Tomo 15 minutos cada mañana para curar lo mejor.

Si trabajas con IA o quieres empezar, te va a ahorrar horas.

#InteligenciaArtificial #IA #Productividad #Tecnología #Innovación
""",
                "hashtags": ["#InteligenciaArtificial", "#IA", "#Productividad", "#Tecnología", "#Innovación"]
            },
            {
                "platform": "pinterest",
                "title": "Herramientas de IA para Productividad 2025",
                "description": f"""
📌 Guía completa de herramientas de IA

Descubre las mejores herramientas de inteligencia artificial para:
✅ Redacción automática
✅ Generación de imágenes
✅ Análisis de datos
✅ Automatización de tareas

🔗 Acceso gratuito en Telegram: {self.channel}

4 posts diarios con:
• Herramientas nuevas
• Tips de productividad
• Recursos gratuitos
• Noticias importantes

¡Síguenos para no perderte nada!

#IA #InteligenciaArtificial #Productividad #HerramientasDigitales #Tecnologia2025
                """,
                "image_text": "50+ Herramientas de IA Gratis - Link en bio"
            }
        ]
    
    def get_promotion_posts_day_2(self) -> list:
        """Día 2: Valor + prueba social"""
        return [
            {
                "platform": "reddit",
                "title": "💡 Recopilé 30 prompts de ChatGPT que realmente funcionan",
                "content": f"""
r/ChatGPT - Después de usar ChatGPT diariamente por 8 meses, estos son los prompts que más me han servido:

**Para escribir:**
"Actúa como [rol experto]. Escribe [contenido] para [audiencia]. El tono debe ser [tono]. Incluye [elementos específicos]."

**Para aprender:**
"Explícame [concepto] como si tuviera 10 años. Usa analogías simples y ejemplos cotidianos. Al final, hazme 3 preguntas para verificar mi comprensión."

**Para código:**
"Escribe una función en [lenguaje] que haga [X]. Incluye comentarios explicando cada parte y ejemplos de uso."

**Para análisis:**
"Analiza el siguiente texto y extrae: 1) Puntos clave 2) Argumentos principales 3) Posibles contraargumentos 4) Conclusión en 1 frase."

...

Tengo 30 prompts más organizados por categoría.

Los comparto todos los días en mi canal de Telegram junto con:
- Herramientas nuevas de IA
- Noticias importantes
- Recursos gratuitos

👉 {self.channel}

¿Cuáles son tus prompts favoritos? ¡Compartan en los comentarios!
""",
                "subreddits": ["ChatGPT", "InteligenciaArtificial", "PromptEngineering"]
            },
            {
                "platform": "twitter",
                "content": f"""
📚 Los 3 mejores recursos GRATIS para aprender IA en 2025:

1️⃣ Learn Prompting (learnprompting.org)
   - Curso completo de prompts
   - Totalmente gratis
   - En español

2️⃣ Hugging Face Courses (huggingface.co/learn)
   - NLP y Machine Learning
   - Con certificados
   - Nivel básico a avanzado

3️⃣ Mi canal de Telegram (@IADailyChannel)
   - 4 posts diarios
   - Herramientas + tips + recursos
   - {self.channel}

¿Cuál agregarías a la lista?

#IA #Educación #Aprendizaje #ChatGPT
""",
                "thread_count": 1
            },
            {
                "platform": "linkedin",
                "content": f"""
📚 5 recursos GRATUITOS para dominar la IA (sin gastar $1)

1. **Learn Prompting** (learnprompting.org)
   El mejor curso en español sobre ingeniería de prompts.

2. **Hugging Face Courses** (huggingface.co/learn)
   Cursos de NLP con certificación incluida.

3. **Google AI Essentials**
   Fundamentos de IA de Google, gratis.

4. **Microsoft Learn AI**
   Ruta de aprendizaje de IA de Microsoft.

5. **IA Daily Channel** (t.me/IADailyChannel)
   Mi canal personal donde comparto diariamente:
   - Herramientas nuevas
   - Tips prácticos
   - Recursos actualizados
   - Noticias importantes

👉 Únete: {self.channel}

La IA está cambiando todo. 
No necesitas pagar miles de dólares para empezar.

Solo necesitas:
✅ Curiosidad
✅ Constancia
✅ Los recursos correctos

¿Qué recurso agregarías a esta lista?

#InteligenciaArtificial #Educación #IA #Aprendizaje #Tecnología
""",
                "hashtags": ["#InteligenciaArtificial", "#Educación", "#IA", "#Aprendizaje", "#Tecnología"]
            },
            {
                "platform": "facebook_groups",
                "content": f"""
🎁 RECURSO GRATIS PARA LA COMUNIDAD

Hola grupo! 👋

Quiero compartir algo que armé para todos los interesados en IA:

**IA Daily Channel** - Un canal de Telegram donde publico 4 veces al día:

🌅 Mañana (08:00) - Herramienta nueva del día
☀️ Mediodía (12:00) - Noticia importante
🌆 Tarde (16:00) - Tip o prompt útil
🌙 Noche (20:00) - Recurso gratuito

¿Por qué lo creé?
Porque me cansé de ver información dispersa y quise tener todo en un solo lugar.

👉 **Únete gratis:** {self.channel}

Actualmente somos [X] miembros compartiendo herramientas y tips.

Es 100% gratis, sin spam, solo contenido de valor.

¿Alguien más usa Telegram para este tipo de contenido?

---
*Si las reglas del grupo no permiten compartir, por favor avisen y lo elimino. Gracias!*
""",
                "groups": ["Inteligencia Artificial en Español", "IA y Machine Learning", "ChatGPT & AI Tools"]
            }
        ]
    
    def get_promotion_posts_day_3(self) -> list:
        """Día 3: Caso de uso específico"""
        return [
            {
                "platform": "reddit",
                "title": "⏰ Cómo la IA me ahorra 10 horas semanales (flujo completo)",
                "content": f"""
r/Productivity - Quiero compartir mi flujo de trabajo con IA que me ahorra ~10 horas por semana:

**Lunes - Planificación (1 hora → 15 min)**
- ChatGPT me ayuda a priorizar tareas
- Uso la matriz de Eisenhower con IA

**Martes - Email (3 horas → 30 min)**
- ChatGPT redacta respuestas base
- Yo solo personalizo el 20%

**Miércoles - Investigación (4 horas → 1 hora)**
- Perplexity.ai encuentra fuentes
- ChatGPT resume los puntos clave

**Jueves - Contenido (2 horas → 30 min)**
- IA genera primeros borradores
- Yo edito y añado mi voz

**Viernes - Análisis (1 hora → 15 min)**
- IA analiza métricas
- Genera insights automáticos

**Total: 11 horas → 2.5 horas = 8.5 horas ahorradas**

Las herramientas específicas que uso las comparto diariamente en mi canal:
👉 {self.channel}

¿Qué herramientas usan ustedes? ¿Alguien tiene flujos similares?

*Nota: No soy experto, solo alguien que prueba cosas hasta encontrar lo que funciona.*
""",
                "subreddits": ["Productivity", "InteligenciaArtificial", "lifehacks"]
            },
            {
                "platform": "twitter",
                "content": f"""
⚠️ 5 errores que cometí aprendiendo IA (para que no los cometas):

1. Querer aprender TODO a la vez
   → Enfócate en 1 herramienta por semana

2. No practicar con casos reales
   → Usa IA en tu trabajo diario

3. Guardar prompts y no organizarlos
   → Crea una biblioteca (yo uso Notion)

4. Seguir "gurús" en vez de practicar
   → La experiencia > teoría

5. Hacerlo solo
   → Únete a comunidades como {self.channel}

¿Cuál cometiste tú?

#IA #Aprendizaje #Productividad
""",
                "thread_count": 1
            },
            {
                "platform": "linkedin",
                "content": f"""
⏰ La IA no me dio más tiempo. Me dio otra vida.

Hace 6 meses trabajaba 60 horas semanales.
Ahora trabajo 40 y produzco el doble.

¿El secreto? No es una herramienta mágica.
Es un SISTEMA.

**Mi sistema de IA en 4 pasos:**

1️⃣ **Captura** - Todo va a una bandeja de entrada
2️⃣ **Procesa** - IA categoriza y prioriza
3️⃣ **Ejecuta** - IA genera primeros borradores
4️⃣ **Refina** - Yo añado el toque humano

**Herramientas clave:**
- ChatGPT: Redacción y análisis
- Notion AI: Organización
- Zapier: Automatización
- [Otras que comparto en mi canal]

**Resultado:**
- 20 horas semanales recuperadas
- Menos estrés
- Mejor calidad de trabajo

Los detalles completos los comparto en mi canal de Telegram:
👉 {self.channel}

Allí publico diariamente:
✅ Herramientas específicas
✅ Flujos de trabajo
✅ Casos de uso reales
✅ Recursos gratuitos

La IA no es el futuro. Es el presente.

¿Ya la estás usando en tu trabajo?

#InteligenciaArtificial #Productividad #IA #Trabajo #Tecnología
""",
                "hashtags": ["#InteligenciaArtificial", "#Productividad", "#IA", "#Trabajo", "#Tecnología"]
            },
            {
                "platform": "pinterest",
                "title": "Flujo de Trabajo con IA - Ahorra 10 Horas Semanales",
                "description": f"""
📌 Infografía: Sistema de productividad con IA

Aprende cómo usar inteligencia artificial para:
✅ Automatizar emails
✅ Generar contenido rápido
✅ Analizar datos automáticamente
✅ Organizar tu semana en minutos

🔗 Guía completa + herramientas: {self.channel}

Canal de Telegram con:
• Tips diarios de productividad
• Herramientas nuevas
• Flujos paso a paso
• Recursos gratuitos

#Productividad #IA #TimeManagement #WorkSmart
                """,
                "image_text": "Ahorra 10 Horas/Semana con IA - Gratis en Telegram"
            }
        ]
    
    def get_promotion_posts_day_4(self) -> list:
        """Día 4: Urgencia + exclusividad"""
        return [
            {
                "platform": "reddit",
                "title": "🎁 Recurso exclusivo: 100+ prompts organizados por categoría",
                "content": f"""
r/ChatGPT - Después de 8 meses usando ChatGPT diariamente, organicé mis mejores prompts:

**Categorías incluidas:**
- 📝 Redacción y contenido (25 prompts)
- 💼 Negocios y marketing (20 prompts)
- 📊 Análisis de datos (15 prompts)
- 🎨 Creatividad e ideas (15 prompts)
- 📚 Aprendizaje y estudio (15 prompts)
- 🔧 Productividad (10 prompts)

**Cada prompt incluye:**
- Contexto de uso
- Variables a modificar
- Ejemplo de resultado

Lo armé en un documento de Notion que comparto GRATIS en mi canal de Telegram:

👉 {self.channel}

Además de los prompts, en el canal comparto:
- Herramientas nuevas de IA cada día
- Noticias importantes (resumidas)
- Tips y trucos que voy descubriendo

Es 100% gratis. Sin spam. Solo contenido que uso personalmente.

¿Qué categoría de prompts les sería más útil?

*Actualización: Ya somos más de [X] miembros compartiendo y mejorando prompts!*
""",
                "subreddits": ["ChatGPT", "InteligenciaArtificial", "Freebies"]
            },
            {
                "platform": "twitter",
                "content": f"""
🚨 ÚLTIMAS HORAS para unirte antes de que llegue a 1K miembros

Mi canal de IA en Telegram está creciendo rápido:

📊 4 posts diarios (sin fallar)
🛠️ 50+ herramientas compartidas
💡 100+ prompts listos para usar
📚 30+ recursos gratuitos

Todo GRATIS. Sin algoritmos. Directo a tu notificación.

👉 {self.channel}

Cuando lleguemos a 1K voy a hacer un sorteo de:
- 3 cuentas premium de herramientas
- Acceso a comunidad VIP
- Plantillas exclusivas

¿Te lo vas a perder?

#IA #ChatGPT #Telegram
""",
                "thread_count": 1
            },
            {
                "platform": "linkedin",
                "content": f"""
🎯 Últimos días para unirte antes del sorteo exclusivo

Mi canal de Telegram sobre IA está a punto de llegar a 1,000 miembros.

Y quiero celebrar con la comunidad que me ha acompañado:

**Sorteo exclusivo para miembros:**
🥇 1er lugar: 3 meses de ChatGPT Plus + Midjourney
🥈 2do lugar: 1 año de Notion Pro
🥉 3er lugar: Pack de plantillas premium

**¿Cómo participar?**
1. Estar en el canal: {self.channel}
2. Compartir el canal con 2 colegas
3. Comentar qué herramienta de IA más te ha ayudado

**¿Qué encontrarás en el canal?**
- 4 posts diarios de contenido verificado
- Herramientas que personalmente pruebo
- Prompts listos para copiar y usar
- Recursos 100% gratuitos

Actualmente somos [X] profesionales compartiendo el día a día con IA.

El sorteo es mi forma de agradecer.

👉 Únete antes del [fecha]: {self.channel}

#InteligenciaArtificial #IA #Sorteo #Comunidad #Tecnología
""",
                "hashtags": ["#InteligenciaArtificial", "#IA", "#Sorteo", "#Comunidad", "#Tecnología"]
            },
            {
                "platform": "facebook_groups",
                "content": f"""
🎁 SORTEO EXCLUSIVO PARA LA COMUNIDAD

¡Hola grupo! 👋

Quiero celebrar que estamos cerca de 1,000 miembros en mi canal de IA.

**Premios:**
🥇 ChatGPT Plus (3 meses) + Midjourney
🥈 Notion Pro (1 año)
🥉 Pack de plantillas premium

**Para participar:**
1. Únete al canal: {self.channel}
2. Invita a 2 colegas
3. Comenta "IA" en este post

**¿Qué hay en el canal?**
- 4 posts diarios con herramientas de IA
- Prompts listos para usar
- Recursos gratuitos
- Noticias importantes (sin clickbait)

Es 100% gratis. El sorteo es mi forma de agradecer.

📅 Sorteo: [fecha]

¿Participas?

---
*Grupo: Si las reglas no permiten sorteos, avisen y edito el post. Gracias!*
""",
                "groups": ["Inteligencia Artificial en Español", "IA y Machine Learning"]
            }
        ]
    
    def get_daily_campaign(self, day: int = None) -> list:
        """Obtener campaña del día"""
        if day is None:
            day = datetime.now().day % 4  # Ciclar entre días 1-4
            if day == 0:
                day = 4
        
        campaigns = {
            1: self.get_promotion_posts_day_1,
            2: self.get_promotion_posts_day_2,
            3: self.get_promotion_posts_day_3,
            4: self.get_promotion_posts_day_4
        }
        
        return campaigns[day]()
    
    def save_campaign(self, posts: list, day: int):
        """Guardar campaña en archivo"""
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = CAMPAIGN_DIR / f"campaign_day{day}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "day": day,
                "date": datetime.now().isoformat(),
                "channel": self.channel,
                "posts": posts,
                "safe_platforms": self.safe_platforms,
                "subreddits": self.telegram_friendly_subreddits
            }, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Campaña guardada: {filename}")
        return filename
    
    async def send_campaign_to_user(self, posts: list, day: int):
        """Enviar campaña al usuario por Telegram"""
        chat_id = self.admin_chat_id

        if not chat_id:
            logger.error("❌ No hay chat_id configurado. Agrega owner_chat_id en config.json")
            return False
        
        # Mensaje de introducción
        intro = f"""
📅 CAMPAÑA DÍA {day} - @IADailyChannel

🎯 4 Posts de PROMOCIÓN listos para hoy

Cada post incluye:
- Título llamativo
- Contenido completo
- Link al canal: {self.channel}
- Plataformas sugeridas

PLATAFORMAS SEGUROS para Telegram:

✅ Twitter/X - Permite links
✅ Reddit - La mayoría de subreddits
✅ LinkedIn - Permite en posts
✅ Pinterest - Permite en pines
✅ YouTube - Descripción y comunidad
⚠️ Instagram - Solo en bio/stories
⚠️ TikTok - Solo en bio
⚠️ Facebook - Depende del grupo

SUBREDDITS RECOMENDADOS:
- r/TelegramChannels (0 karma)
- r/InteligenciaArtificial (0 karma)
- r/IA (0 karma)
- r/ChatGPT (50 karma)
- r/Productivity (100 karma)
- r/Freebies (100 karma)

Posts completos abajo
        """
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=intro,
                parse_mode=None
            )
            
            # Enviar cada post
            for i, post in enumerate(posts, 1):
                platform = post.get("platform", "general")
                title = post.get("title", f"Post {i}")
                content = post.get("content", "")

                message = f"""
📱 {platform.upper()} - Post {i}/{len(posts)}

Título: {title}

{content}

---

Copia y pega en {platform}
                """

                # Enviar sin parse_mode para evitar errores con contenido dinámico
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=None
                )
                await asyncio.sleep(0.5)
            
            # Resumen final
            outro = f"""
✅ CAMPAÑA DÍA {day} COMPLETA

Resumen:
- Posts generados: {len(posts)}
- Plataformas: Twitter, Reddit, LinkedIn, Pinterest
- Link del canal incluido en todos

Acción recomendada:
1. Copia cada post
2. Pega en la plataforma correspondiente
3. Responde comentarios (importante!)
4. Vuelve mañana para nueva campaña

Archivo guardado:
campaign_day{day}_{datetime.now().strftime('%Y%m%d')}.json

Para ejecutar manualmente:
python campaign_manager.py
            """

            await self.bot.send_message(
                chat_id=chat_id,
                text=outro,
                parse_mode=None
            )
            
            logger.info(f"✅ Campaña día {day} enviada a Telegram")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al enviar: {e}")
            return False
    
    async def run_campaign(self):
        """Ejecutar campaña completa"""
        print("=" * 50)
        print("🚀 Campaign Manager - IA Daily")
        print("=" * 50)
        
        # Determinar día
        day = datetime.now().day % 4
        if day == 0:
            day = 4
        
        print(f"\n📅 Generando campaña para DÍA {day}...")
        
        # Obtener posts
        posts = self.get_daily_campaign(day)
        
        print(f"✅ {len(posts)} posts generados")
        
        # Guardar campaña
        self.save_campaign(posts, day)
        
        # Enviar a Telegram
        print("\n📤 Enviando a tu Telegram...")
        success = await self.send_campaign_to_user(posts, day)
        
        if success:
            print("\n✅ ¡Campaña enviada!")
            print("\n📱 Revisa Telegram para ver los posts completos")
        else:
            print("\n⚠️ Error al enviar. Revisa los logs.")
        
        return posts


async def main():
    manager = CampaignManager()
    await manager.run_campaign()


if __name__ == '__main__':
    asyncio.run(main())
