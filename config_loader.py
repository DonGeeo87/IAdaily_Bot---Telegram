#!/usr/bin/env python3
"""
Utilidad para cargar configuración desde variables de entorno
Compatible con fly.io y otros proveedores de nube
"""

import os
import json
from pathlib import Path


def get_env_config():
    """
    Cargar configuración desde variables de entorno.
    Prioridad: Variables de entorno > config.json
    """
    config = {}
    
    # Telegram
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        config["telegram"] = config.get("telegram", {})
        config["telegram"]["bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
        
    if os.getenv("TELEGRAM_CHANNEL_ID"):
        config["telegram"] = config.get("telegram", {})
        config["telegram"]["channel_id"] = os.getenv("TELEGRAM_CHANNEL_ID")
        
    if os.getenv("TELEGRAM_ADMIN_USERS"):
        config["telegram"] = config.get("telegram", {})
        config["telegram"]["admin_users"] = [
            int(x.strip()) for x in os.getenv("TELEGRAM_ADMIN_USERS").split(",")
        ]
    
    # Zona horaria
    if os.getenv("TIMEZONE"):
        config["schedule"] = config.get("schedule", {})
        config["schedule"]["timezone"] = os.getenv("TIMEZONE")
    
    # Nivel de log
    if os.getenv("LOG_LEVEL"):
        config["features"] = config.get("features", {})
        config["features"]["log_level"] = os.getenv("LOG_LEVEL")
    
    # APIs de IA
    for api in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "QWEN_API_KEY"]:
        if os.getenv(api):
            config["apis"] = config.get("apis", {})
            config["apis"][api.lower()] = os.getenv(api)
    
    return config


def merge_config(file_config: dict, env_config: dict) -> dict:
    """
    Fusionar configuración: variables de entorno tienen prioridad
    """
    result = file_config.copy()
    
    # Fusionar telegram
    if "telegram" in env_config:
        result["telegram"] = {**result.get("telegram", {}), **env_config["telegram"]}
    
    # Fusionar schedule
    if "schedule" in env_config:
        result["schedule"] = {**result.get("schedule", {}), **env_config["schedule"]}
    
    # Fusionar features
    if "features" in env_config:
        result["features"] = {**result.get("features", {}), **env_config["features"]}
    
    # Fusionar apis
    if "apis" in env_config:
        result["apis"] = {**result.get("apis", {}), **env_config["apis"]}
    
    return result


def load_config_with_env(config_file: str = "config.json") -> dict:
    """
    Cargar configuración desde archivo + variables de entorno
    """
    config_path = Path(config_file)
    
    # Cargar desde archivo
    file_config = {}
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            file_config = json.load(f)
    
    # Cargar desde variables de entorno
    env_config = get_env_config()
    
    # Fusionar (env tiene prioridad)
    return merge_config(file_config, env_config)


def validate_config(config: dict) -> tuple:
    """
    Validar configuración requerida
    Returns: (es_valido, mensaje_error)
    """
    errors = []
    
    # Telegram token
    if not config.get("telegram", {}).get("bot_token"):
        errors.append("❌ Telegram bot token faltante (TELEGRAM_BOT_TOKEN)")
    
    # Channel ID
    if not config.get("telegram", {}).get("channel_id"):
        errors.append("❌ Telegram channel ID faltante (TELEGRAM_CHANNEL_ID)")
    
    # Admin users
    if not config.get("telegram", {}).get("admin_users"):
        errors.append("⚠️  No hay admin users configurados (TELEGRAM_ADMIN_USERS)")
    
    if errors:
        return False, "\n".join(errors)
    
    return True, "Configuración válida"


if __name__ == "__main__":
    # Test de la utilidad
    print("🔧 Test de configuración con variables de entorno")
    print("=" * 50)
    
    config = load_config_with_env()
    valid, msg = validate_config(config)
    
    print(f"\nEstado: {'✅ Válida' if valid else '❌ Inválida'}")
    print(f"\n{msg}")
    
    if valid:
        print(f"\n📢 Canal: {config['telegram']['channel_id']}")
        print(f"🔑 Token: {'*' * 20}{config['telegram']['bot_token'][-10:]}")
        print(f"👥 Admins: {config['telegram']['admin_users']}")
