#!/usr/bin/env python3
"""
📱 Social Media Auto-Poster
Publica automáticamente en múltiples plataformas
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path

try:
    from telegram import Bot
except ImportError:
    print("Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot


class SocialMediaAutoPoster:
    """Publicador automático en redes sociales"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "config.json"
        self.config = self.load_config()
        self.channel = "https://t.me/IADailyChannel"
        
    def load_config(self) -> dict:
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def format_for_twitter(self, content: str) -> str:
        """Formatear contenido para Twitter (280 chars)"""
        hashtags = [
            "#IA",
            "#InteligenciaArtificial", 
            "#AI",
            "#TechNews",
            "#AIEspañol"
        ]
        
        # Truncar si es muy largo
        max_length = 280 - len(" ".join(hashtags)) - 3
        if len(content) > max_length:
            content = content[:max_length-3] + "..."
        
        return f"{content}\n\n{' '.join(hashtags)}\n\n👉 {self.channel}"
    
    def format_for_linkedin(self, content: str) -> str:
        """Formatear para LinkedIn (más profesional)"""
        return f"""🤖 IA Daily Channel

{content}

Síguenos para más contenido sobre Inteligencia Artificial.

🔗 {self.channel}

#InteligenciaArtificial #IA #Tecnología #Innovación #AI
"""
    
    def format_for_instagram(self, content: str) -> str:
        """Formatear para Instagram (caption)"""
        hashtags = """
#ia #inteligenciaartificial #ai #artificialintelligence 
#tecnologia #innovation #tech #machinelearning #deeplearning 
#chatgpt #openai #programming #coding #technews #futuro 
#automatizacion #aiart #midjourney #promptengineering
"""
        return f"{content}\n\n👉 Link en bio: t.me/IADailyChannel\n\n{hashtags}"
    
    def format_for_tiktok(self, content: str) -> str:
        """Script para TikTok (video corto)"""
        return f"""
🎬 GUION TIKTOK (30 segundos)

[0-3s] Hook: "¿Sabías que esta IA puede hacer [X]?"
[3-15s] Demo: Mostrar herramienta/caso de uso
[15-25s] Valor: Explicar beneficio principal
[25-30s] CTA: "Síguenos en Telegram para más → Link en bio"

📝 Contenido:
{content[:200]}

🔗 {self.channel}
"""
    
    def format_for_reddit(self, title: str, content: str, subreddit: str) -> dict:
        """Formatear para Reddit"""
        return {
            "subreddit": subreddit,
            "title": title,
            "content": f"""{content}

---

💡 *Más contenido diario en nuestro canal de Telegram:* {self.channel}

*Post relacionado con IA y tecnología*
""",
            "flair": "Recursos" if "recurso" in content.lower() else "Noticia"
        }
    
    def generate_daily_posts(self) -> dict:
        """Generar posts para todas las plataformas"""
        
        # Contenido base del día
        base_content = {
            "twitter": self.format_for_twitter(
                "🚀 Nueva herramienta de IA que debes conocer hoy. "
                "Te ahorra horas de trabajo automatizando tareas repetitivas. "
                "¡Totalmente gratis!"
            ),
            "linkedin": self.format_for_linkedin(
                "La inteligencia artificial está transformando la forma en que trabajamos. "
                "En nuestro canal compartimos diariamente:\n\n"
                "• Herramientas prácticas\n"
                "• Noticias relevantes\n"
                "• Tips de productividad\n"
                "• Recursos gratuitos\n\n"
                "Ideal para profesionales que quieren mantenerse actualizados."
            ),
            "instagram": self.format_for_instagram(
                "🤖 ¿Listo para dominar la IA?\n\n"
                "Cada día compartimos:\n"
                "✅ Herramientas nuevas\n"
                "✅ Tips que funcionan\n"
                "✅ Recursos 100% gratis\n\n"
                "Únete a la comunidad hispana de IA más activa!"
            ),
            "tiktok": self.format_for_tiktok(
                "Herramienta IA del día que te va a volar la cabeza 🤯"
            ),
            "facebook": self.format_for_linkedin(
                "¿Te interesa la Inteligencia Artificial pero no tienes tiempo de buscar información?\n\n"
                "Nosotros lo hacemos por ti. 4 posts diarios con lo más importante.\n\n"
                "¡Únete gratis!"
            )
        }
        
        return base_content
    
    def save_posts(self):
        """Guardar posts generados"""
        posts = self.generate_daily_posts()
        
        output_dir = Path(__file__).parent / "social_posts"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        
        for platform, content in posts.items():
            filename = output_dir / f"{timestamp}_{platform}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {platform}: {filename}")
        
        return posts
    
    def get_posting_schedule(self) -> dict:
        """Obtener horario óptimo de publicación"""
        return {
            "twitter": ["09:00", "13:00", "18:00", "21:00"],
            "linkedin": ["08:00", "12:00", "17:00"],
            "instagram": ["10:00", "15:00", "20:00"],
            "tiktok": ["11:00", "16:00", "21:00"],
            "facebook": ["09:00", "14:00", "19:00"],
            "reddit": ["10:00", "15:00", "20:00"]
        }


def main():
    print("=" * 50)
    print("📱 Social Media Auto-Poster")
    print("=" * 50)
    
    poster = SocialMediaAutoPoster()
    posts = poster.save_posts()
    
    print("\n⏰ Horario óptimo de publicación:")
    schedule = poster.get_posting_schedule()
    for platform, times in schedule.items():
        print(f"   {platform}: {', '.join(times)}")
    
    print("\n💡 Tip: Copia y pega estos posts en cada plataforma")
    print("   o usa herramientas como Buffer/Hootsuite para automatizar")


if __name__ == '__main__':
    main()
