#!/usr/bin/env python3
"""
📝 Content Generator - Generador automático de contenido sobre IA
Obtiene noticias, herramientas y recursos de fuentes RSS/APIs
"""

import os
import sys
import json
import random
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import feedparser
except ImportError:
    print("📦 Instalando feedparser...")
    os.system("pip install feedparser")
    import feedparser

try:
    import requests
except ImportError:
    print("📦 Instalando requests...")
    os.system("pip install requests")
    import requests

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
LOGS_DIR = BASE_DIR / "logs"
POSTS_DIR = BASE_DIR / "posts"

# Logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"generator_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generador de contenido automático sobre IA"""
    
    def __init__(self):
        self.config = self.load_config()
        self.sources_config = self.load_sources_config()
        self.language = self.config["content"]["language"]
        
        # Fuentes adicionales de noticias de IA
        self.ia_sources = self.sources_config.get("fuentes_noticias", [])
        
        # Plantillas de contenido
        self.templates = self.load_templates()
    
    def load_config(self) -> dict:
        """Cargar configuración"""
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_sources_config(self) -> dict:
        """Cargar configuración de fuentes de contenido"""
        sources_file = BASE_DIR / "content_sources.json"
        if sources_file.exists():
            with open(sources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_templates(self) -> dict:
        """Cargar plantillas de contenido"""
        return {
            "herramienta": """
🛠️ <b>Herramienta IA del Día</b>

📌 <b>{name}</b>

{description}

🔗 Enlace: {url}

💡 <i>Ideal para:</i> {use_case}

{footer}
            """,
            "noticia": """
📰 <b>Noticia IA</b>

<b>{title}</b>

{summary}

📖 Leer más: {url}

{footer}
            """,
            "tip": """
💡 <b>Tip IA del Día</b>

{tip}

📝 <b>Ejemplo:</b>
{example}

{footer}
            """,
            "recurso": """
📦 <b>Recurso Gratuito</b>

📚 <b>{name}</b>

{description}

🎁 <i>Gratis por tiempo limitado</i>

👉 Descarga: {url}

{footer}
            """,
            "prompt": """
🎯 <b>Prompt del Día</b>

<b>Objetivo:</b> {goal}

<b>Prompt:</b>
<code>{prompt}</code>

<b>Consejo:</b> {tip}

{footer}
            """
        }
    
    def fetch_rss(self, url: str) -> List[Dict]:
        """Obtener entradas de feed RSS"""
        try:
            feed = feedparser.parse(url)
            entries = []
            
            for entry in feed.entries[:5]:  # Máximo 5 entradas por fuente
                entries.append({
                    "title": entry.get("title", "Sin título"),
                    "summary": entry.get("summary", entry.get("description", ""))[:200],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": feed.feed.get("title", "Unknown")
                })
            
            logger.info(f"✅ {len(entries)} entradas de {url}")
            return entries
            
        except Exception as e:
            logger.error(f"❌ Error fetching {url}: {e}")
            return []
    
    def fetch_all_sources(self) -> List[Dict]:
        """Obtener contenido de todas las fuentes"""
        all_entries = []
        
        for source in self.ia_sources:
            entries = self.fetch_rss(source)
            all_entries.extend(entries)
        
        # Mezclar y devolver
        random.shuffle(all_entries)
        return all_entries
    
    def generate_herramienta(self) -> str:
        """Generar post de herramienta IA"""
        herramientas = [
            {
                "name": "ChatGPT",
                "description": "El asistente de IA más popular del mundo. Ahora con capacidades multimodales.",
                "url": "https://chat.openai.com",
                "use_case": "Redacción, código, análisis, creatividad"
            },
            {
                "name": "Midjourney",
                "description": "Generador de imágenes artísticas mediante IA desde Discord.",
                "url": "https://midjourney.com",
                "use_case": "Arte digital, concept art, ilustraciones"
            },
            {
                "name": "Notion AI",
                "description": "IA integrada en Notion para mejorar tu productividad.",
                "url": "https://notion.so/ai",
                "use_case": "Notas, documentos, organización"
            },
            {
                "name": "GitHub Copilot",
                "description": "Tu programador par con IA. Autocompleta código en tiempo real.",
                "url": "https://github.com/features/copilot",
                "use_case": "Programación, debugging, aprendizaje"
            },
            {
                "name": "Runway ML",
                "description": "Suite de herramientas de IA para creación de video.",
                "url": "https://runwayml.com",
                "use_case": "Edición de video, efectos, generación"
            }
        ]
        
        tool = random.choice(herramientas)
        return self.templates["herramienta"].format(
            **tool,
            footer=self.config["branding"]["footer"]
        )
    
    def generate_noticia(self, entry: Dict = None) -> str:
        """Generar post de noticia"""
        if not entry:
            # Noticia genérica si no hay entrada
            entry = {
                "title": "La IA continúa transformando industrias",
                "summary": "Nuevos avances en inteligencia artificial están revolucionando sectores como salud, educación y tecnología.",
                "url": "https://news.ycombinator.com"
            }
        
        # Asegurar que tenga url
        if "url" not in entry:
            entry["url"] = entry.get("link", "https://news.ycombinator.com")
        
        return self.templates["noticia"].format(
            **entry,
            footer=self.config["branding"]["footer"]
        )
    
    def generate_tip(self) -> str:
        """Generar tip útil sobre IA"""
        tips = [
            {
                "tip": "Usa prompts específicos con contexto para obtener mejores resultados de IA.",
                "example": "En lugar de 'escribe un email', usa 'escribe un email profesional para solicitar una reunión con un cliente potencial en el sector tech'"
            },
            {
                "tip": "Divide tareas complejas en pasos más pequeños cuando uses IA.",
                "example": "Primero pide un esquema, luego desarrolla cada sección por separado"
            },
            {
                "tip": "Proporciona ejemplos en tu prompt para guiar el estilo de respuesta.",
                "example": "Incluye 2-3 ejemplos del formato que esperas obtener"
            },
            {
                "tip": "Usa 'piensa paso a paso' para problemas de lógica o matemáticas.",
                "example": "Añade esta frase al final de tu prompt para mejorar la precisión"
            },
            {
                "tip": "Itera sobre los resultados. La primera respuesta rara vez es la mejor.",
                "example": "Pide refinamientos: 'mejora esto', 'hazlo más conciso', 'añade ejemplos'"
            }
        ]
        
        tip = random.choice(tips)
        return self.templates["tip"].format(
            **tip,
            footer=self.config["branding"]["footer"]
        )
    
    def generate_recurso(self) -> str:
        """Generar post de recurso gratuito"""
        recursos = [
            {
                "name": "Curso de Prompt Engineering",
                "description": "Aprende a crear prompts efectivos para cualquier modelo de IA.",
                "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/"
            },
            {
                "name": "Awesome ChatGPT Prompts",
                "description": "Repositorio con cientos de prompts listos para usar.",
                "url": "https://github.com/f/awesome-chatgpt-prompts"
            },
            {
                "name": "Hugging Face Courses",
                "description": "Cursos gratuitos de NLP y Machine Learning.",
                "url": "https://huggingface.co/learn"
            },
            {
                "name": "Learn Prompting",
                "description": "Guía completa y gratuita sobre ingeniería de prompts.",
                "url": "https://learnprompting.org"
            }
        ]
        
        recurso = random.choice(recursos)
        return self.templates["recurso"].format(
            **recurso,
            footer=self.config["branding"]["footer"]
        )
    
    def generate_prompt_del_dia(self) -> str:
        """Generar prompt del día"""
        prompts = [
            {
                "goal": "Crear contenido para redes sociales",
                "prompt": "Actúa como un experto en marketing digital. Crea 5 posts para LinkedIn sobre [TEMA] que sean informativos, engagement y profesionales. Incluye emojis apropiados y un call-to-action al final.",
                "tip": "Reemplaza [TEMA] con tu nicho específico"
            },
            {
                "goal": "Aprender un concepto nuevo",
                "prompt": "Explícame [CONCEPTO] como si tuviera 10 años. Usa analogías simples y ejemplos cotidianos. Al final, hazme 3 preguntas para verificar mi comprensión.",
                "tip": "Ideal para estudiar rápido"
            },
            {
                "goal": "Mejorar un texto",
                "prompt": "Revisa el siguiente texto y: 1) Corrige errores gramaticales 2) Mejora la claridad 3) Sugiere 3 alternativas de estilo. Texto: [PEGAR TEXTO]",
                "tip": "Útil para emails y documentos"
            },
            {
                "goal": "Generar ideas de negocio",
                "prompt": "Soy experto en [HABILIDAD] y me interesa [INDUSTRIA]. Genera 10 ideas de negocio que combinen ambos, con modelo de ingresos potencial y primer paso accionable.",
                "tip": "Combina tus skills con mercados rentables"
            }
        ]
        
        prompt = random.choice(prompts)
        return self.templates["prompt"].format(
            **prompt,
            footer=self.config["branding"]["footer"]
        )
    
    def generate_all(self) -> Dict[str, str]:
        """Generar todo el contenido del día"""
        return {
            "herramienta": self.generate_herramienta(),
            "noticia": self.generate_noticia(),
            "tip": self.generate_tip(),
            "recurso": self.generate_recurso(),
            "prompt": self.generate_prompt_del_dia()
        }
    
    def save_posts(self, posts: Dict[str, str]):
        """Guardar posts generados en archivos"""
        timestamp = datetime.now().strftime("%Y%m%d")
        
        for post_type, content in posts.items():
            filename = POSTS_DIR / f"{timestamp}_{post_type}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Guardado: {filename}")
    
    def run(self):
        """Ejecutar generador"""
        print(f"📝 Generando contenido para {self.config['branding']['bot_name']}...")
        
        posts = self.generate_all()
        self.save_posts(posts)
        
        print(f"\n✅ {len(posts)} posts generados:")
        for post_type in posts.keys():
            print(f"   - {post_type}")
        
        print(f"\n📁 Guardados en: {POSTS_DIR}")
        
        return posts


def main():
    generator = ContentGenerator()
    generator.run()


if __name__ == '__main__':
    main()
