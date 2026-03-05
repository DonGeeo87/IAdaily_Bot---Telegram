#!/usr/bin/env python3
"""
📈 Growth Tracker - Monitor de crecimiento del canal
Trackea suscriptores, engagement y métricas virales
"""

import os
import sys
import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

try:
    from telegram import Bot
except ImportError:
    print("Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot


class GrowthTracker:
    """Monitor de crecimiento del canal"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "config.json"
        self.config = self.load_config()
        self.token = self.config.get("telegram", {}).get("bot_token", "")
        self.channel = self.config.get("telegram", {}).get("channel_id", "")
        self.stats_file = Path(__file__).parent / "growth_stats.json"
        
    def load_config(self) -> dict:
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def get_channel_stats(self) -> dict:
        """Obtener estadísticas del canal"""
        if not self.token:
            return {"error": "Token no configurado"}
        
        bot = Bot(token=self.token)
        
        try:
            # Obtener información del canal
            chat = await bot.get_chat(self.channel)
            
            stats = {
                "title": chat.title,
                "username": chat.username,
                "subscribers": chat.members_count if hasattr(chat, 'members_count') else 0,
                "description": chat.description[:100] if chat.description else "",
                "photo": chat.photo is not None,
                "timestamp": datetime.now().isoformat()
            }
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
    
    def load_history(self) -> list:
        """Cargar historial de estadísticas"""
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_stats(self, stats: dict):
        """Guardar estadísticas en historial"""
        history = self.load_history()
        history.append(stats)
        
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def calculate_growth(self) -> dict:
        """Calcular crecimiento"""
        history = self.load_history()
        
        if len(history) < 2:
            return {"message": "Insuficientes datos para calcular crecimiento"}
        
        # Últimos 7 días
        recent = history[-7:] if len(history) >= 7 else history
        
        if len(recent) < 2:
            return {"message": "Se necesitan al menos 2 registros"}
        
        first = recent[0].get("subscribers", 0)
        last = recent[-1].get("subscribers", 0)
        
        growth = last - first
        growth_percent = ((last - first) / first * 100) if first > 0 else 0
        
        daily_avg = growth / len(recent) if len(recent) > 0 else 0
        
        return {
            "period_days": len(recent),
            "start_subscribers": first,
            "current_subscribers": last,
            "total_growth": growth,
            "growth_percent": round(growth_percent, 2),
            "daily_average": round(daily_avg, 2),
            "projected_30_days": round(last + (daily_avg * 30), 0)
        }
    
    def get_viral_metrics(self) -> dict:
        """Obtener métricas virales"""
        return {
            "share_rate": "N/A (requiere API premium)",
            "forward_rate": "N/A (requiere API premium)",
            "engagement_tips": [
                "Publica a horas consistentes",
                "Usa emojis en los títulos",
                "Incluye llamadas a la acción",
                "Comparte contenido exclusivo",
                "Responde a comentarios en posts relacionados"
            ]
        }
    
    async def run_tracker(self):
        """Ejecutar tracker y mostrar resultados"""
        print("=" * 50)
        print("📈 IA Daily - Growth Tracker")
        print("=" * 50)
        
        # Obtener stats actuales
        print("\n📊 Obteniendo estadísticas...")
        stats = await self.get_channel_stats()
        
        if "error" in stats:
            print(f"❌ Error: {stats['error']}")
            return
        
        # Guardar stats
        self.save_stats(stats)
        
        # Mostrar información
        print(f"\n📢 Canal: @{stats.get('username', 'N/A')}")
        print(f"👥 Suscriptores: {stats.get('subscribers', 0):,}")
        print(f"📝 Descripción: {stats.get('description', 'N/A')[:50]}...")
        
        # Calcular crecimiento
        print("\n📈 Crecimiento:")
        growth = self.calculate_growth()
        if "message" in growth:
            print(f"   ⏳ {growth['message']}")
        else:
            print(f"   📊 Período: {growth['period_days']} días")
            print(f"   📈 Crecimiento total: +{growth['total_growth']} suscriptores")
            print(f"   📊 Porcentaje: {growth['growth_percent']}%")
            print(f"   📈 Promedio diario: +{growth['daily_average']} suscriptores/día")
            print(f"   🔮 Proyección 30 días: {growth['projected_30_days']:,.0f} suscriptores")
        
        # Métricas virales
        print("\n🚀 Tips para crecimiento viral:")
        viral = self.get_viral_metrics()
        for tip in viral['engagement_tips']:
            print(f"   ✅ {tip}")
        
        return stats


async def main():
    tracker = GrowthTracker()
    await tracker.run_tracker()


if __name__ == '__main__':
    asyncio.run(main())
