#!/usr/bin/env python3
"""
📊 Analytics Dashboard - Métricas en tiempo real del canal
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

try:
    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
except ImportError:
    print("Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
ANALYTICS_FILE = BASE_DIR / "analytics_data.json"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"analytics_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AnalyticsDashboard:
    """Dashboard de métricas del canal"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = Bot(token=self.token)
        self.data = self.load_analytics()
        
    def load_config(self) -> dict:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_analytics(self) -> dict:
        """Cargar datos de analytics"""
        default_data = {
            "posts": [],
            "polls": [],
            "engagement": [],
            "new_members": [],
            "daily_stats": {}
        }
        
        if ANALYTICS_FILE.exists():
            with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                for key in default_data:
                    if key not in saved_data:
                        default_data[key] = saved_data.get(key, default_data[key])
        
        return default_data
    
    def save_analytics(self):
        """Guardar datos de analytics"""
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    async def get_channel_stats(self) -> dict:
        """Obtener estadísticas del canal"""
        try:
            chat = await self.bot.get_chat(self.channel)
            
            stats = {
                "title": chat.title,
                "username": chat.username,
                "members_count": chat.members_count,
                "description": chat.description[:100] if chat.description else "",
                "photo": chat.photo is not None,
                "invite_link": chat.invite_link if hasattr(chat, 'invite_link') else None
            }
            
            return stats
        except Exception as e:
            logger.error(f"Error al obtener stats: {e}")
            return {}
    
    def track_post(self, post_type: str, views: int = 0, shares: int = 0):
        """Registrar post publicado"""
        post = {
            "timestamp": datetime.now().isoformat(),
            "type": post_type,
            "views": views,
            "shares": shares
        }
        
        self.data["posts"].append(post)
        
        # Mantener solo últimos 100 posts
        if len(self.data["posts"]) > 100:
            self.data["posts"] = self.data["posts"][-100:]
        
        self.save_analytics()
        logger.info(f"📝 Post registrado: {post_type}")
    
    def track_poll(self, question: str, votes: int):
        """Registrar encuesta"""
        poll = {
            "timestamp": datetime.now().isoformat(),
            "question": question[:50],
            "votes": votes
        }
        
        self.data["polls"].append(poll)
        
        # Mantener solo últimas 50 encuestas
        if len(self.data["polls"]) > 50:
            self.data["polls"] = self.data["polls"][-50:]
        
        self.save_analytics()
        logger.info(f"📊 Encuesta registrada: {votes} votos")
    
    def track_engagement(self, action: str, count: int):
        """Registrar acción de engagement"""
        engagement = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "count": count
        }
        
        self.data["engagement"].append(engagement)
        
        # Mantener solo últimos 200 registros
        if len(self.data["engagement"]) > 200:
            self.data["engagement"] = self.data["engagement"][-200:]
        
        self.save_analytics()
    
    def get_daily_stats(self, days: int = 7) -> dict:
        """Obtener estadísticas de los últimos N días"""
        now = datetime.now()
        cutoff = now - timedelta(days=days)
        
        # Filtrar posts por fecha
        recent_posts = [
            p for p in self.data["posts"]
            if datetime.fromisoformat(p["timestamp"]) > cutoff
        ]
        
        # Filtrar encuestas
        recent_polls = [
            p for p in self.data["polls"]
            if datetime.fromisoformat(p["timestamp"]) > cutoff
        ]
        
        # Calcular métricas
        total_posts = len(recent_posts)
        total_polls = len(recent_polls)
        total_votes = sum(p.get("votes", 0) for p in recent_polls)
        
        # Posts por tipo
        posts_by_type = defaultdict(int)
        for post in recent_posts:
            posts_by_type[post.get("type", "unknown")] += 1
        
        # Engagement promedio
        avg_engagement = total_votes / total_polls if total_polls > 0 else 0
        
        return {
            "period_days": days,
            "total_posts": total_posts,
            "total_polls": total_polls,
            "total_votes": total_votes,
            "avg_engagement": round(avg_engagement, 2),
            "posts_by_type": dict(posts_by_type)
        }
    
    def get_growth_rate(self) -> dict:
        """Calcular tasa de crecimiento"""
        # Obtener miembros actuales
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        stats = loop.run_until_complete(self.get_channel_stats())
        loop.close()
        
        current_members = stats.get("members_count", 0)
        
        # Calcular crecimiento diario promedio
        if self.data.get("new_members"):
            recent_members = self.data["new_members"][-7:]  # Última semana
            avg_daily_growth = len(recent_members) / 7 if recent_members else 0
        else:
            avg_daily_growth = 0
        
        # Proyección a 30 días
        projected_30_days = current_members + (avg_daily_growth * 30)
        
        return {
            "current_members": current_members,
            "avg_daily_growth": round(avg_daily_growth, 2),
            "projected_30_days": round(projected_30_days, 0),
            "growth_rate": round((avg_daily_growth / current_members * 100) if current_members > 0 else 0, 2)
        }
    
    def generate_report(self) -> str:
        """Generar reporte completo"""
        stats = asyncio.run(self.get_channel_stats())
        daily_stats = self.get_daily_stats(7)
        growth = self.get_growth_rate()
        
        report = f"""
📊 **REPORTE ANALYTICS - {stats.get('title', self.channel)}**

👥 **MIEMBROS:**
• Actuales: {growth['current_members']:,}
• Crecimiento diario: +{growth['avg_daily_growth']}
• Proyección 30 días: {growth['projected_30_days']:,.0f}
• Tasa de crecimiento: {growth['growth_rate']}%

📝 **CONTENIDO (Últimos 7 días):**
• Posts publicados: {daily_stats['total_posts']}
• Encuestas: {daily_stats['total_polls']}
• Votos en encuestas: {daily_stats['total_votes']}
• Engagement promedio: {daily_stats['avg_engagement']} votos/encuesta

📈 **POSTS POR TIPO:**
"""
        
        for post_type, count in daily_stats['posts_by_type'].items():
            emoji = {"herramienta": "🛠️", "noticia": "📰", "tip": "💡", "recurso": "📦", "prompt": "🎯"}.get(post_type, "📌")
            report += f"• {emoji} {post_type.title()}: {count}\n"
        
        report += f"""
🎯 **MÉTRICAS DE ENGAGEMENT:**
• Encuestas: {daily_stats['total_polls']}
• Desafíos: {len([e for e in self.data.get('engagement', []) if e.get('action') == 'challenge'])}
• Preguntas: {len([e for e in self.data.get('engagement', []) if e.get('action') == 'question'])}

💡 **RECOMENDACIONES:**
"""
        
        # Generar recomendaciones basadas en datos
        if daily_stats['total_posts'] < 20:
            report += "• ⚠️ Publicar más contenido (objetivo: 28 posts/semana)\n"
        
        if daily_stats['avg_engagement'] < 50:
            report += "• ⚠️ Mejorar engagement (hacer más preguntas)\n"
        
        if growth['avg_daily_growth'] < 10:
            report += "• ⚠️ Acelerar promoción (publicar en más redes)\n"
        
        if daily_stats['avg_engagement'] >= 100:
            report += "• ✅ ¡Excelente engagement! Seguir así\n"
        
        if growth['avg_daily_growth'] >= 20:
            report += "• ✅ ¡Gran crecimiento! Continuar promoción\n"
        
        return report
    
    async def send_report(self, chat_id: int):
        """Enviar reporte a un chat"""
        report = self.generate_report()
        
        keyboard = [
            [InlineKeyboardButton("🔄 Actualizar", callback_data="analytics_refresh")],
            [InlineKeyboardButton("📈 Últimos 30 días", callback_data="analytics_30d")],
            [InlineKeyboardButton("📊 Exportar JSON", callback_data="analytics_export")]
        ]
        
        await self.bot.send_message(
            chat_id=chat_id,
            text=report,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


def main():
    print("📊 Analytics Dashboard listo!")
    print("\nPara ver métricas usa el comando:")
    print("  /analytics en Telegram")
    print("\nO ejecuta:")
    print("  python analytics_dashboard.py --report")


if __name__ == '__main__':
    main()
