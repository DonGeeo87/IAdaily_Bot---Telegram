#!/usr/bin/env python3
"""
🤖 Qwen AI Integration - IA Real para el bot
Usa la API de Qwen para generar contenido inteligente
"""

import os
import json
import aiohttp
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Configuración
BASE_DIR = Path(__file__).parent
QWEN_CONFIG_FILE = BASE_DIR / "qwen_config.json"


class QwenAI:
    """Integración con API de Qwen (Alibaba Cloud DashScope)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Endpoint oficial de DashScope
        self.base_url = "https://dashscope-intl.aliyuncs.com/api/v1"
        # Alternativa: https://dashscope.aliyuncs.com/api/v1
        self.model = "qwen-turbo"
        
    async def generate_text(self, prompt: str, max_tokens: int = 500) -> str:
        """Generar texto con Qwen"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en Inteligencia Artificial. Respondes de forma clara, concisa y útil en español."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            },
            "parameters": {
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Usar endpoint internacional
                url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("output", {}).get("text", "")
                    else:
                        error_text = await response.text()
                        logger.error(f"Error Qwen API: {response.status} - {error_text}")
                        return f"❌ Error API: {response.status}"
                        
        except Exception as e:
            logger.error(f"Error al conectar con Qwen: {e}")
            return f"❌ Error de conexión: {e}"
    
    async def generate_news_summary(self, topic: str) -> str:
        """Generar resumen de noticias sobre un tema"""
        prompt = f"""
Genera un resumen de noticias sobre: {topic}

Incluye:
1. Título llamativo
2. 3 puntos clave
3. Por qué es importante
4. Enlace sugerido para más info

Formato para Telegram (usa emojis, HTML básico).
Máximo 300 palabras.
        """
        
        return await self.generate_text(prompt)
    
    async def generate_tool_review(self, tool_name: str) -> str:
        """Generar review de herramienta de IA"""
        prompt = f"""
Genera una review completa de la herramienta de IA: {tool_name}

Incluye:
1. ¿Qué es? (2-3 líneas)
2. Características principales (3-5 bullets)
3. Casos de uso (2-3 ejemplos)
4. Precio (si es gratis mencionar)
5. Enlace oficial

Formato para Telegram con emojis.
Máximo 400 palabras.
        """
        
        return await self.generate_text(prompt)
    
    async def generate_prompt_chatgpt(self, category: str) -> str:
        """Generar prompt para ChatGPT"""
        prompt = f"""
Crea un prompt avanzado para ChatGPT sobre: {category}

El prompt debe:
1. Tener contexto claro
2. Especificar el rol de la IA
3. Incluir formato de salida esperado
4. Tener ejemplo de uso

Formato listo para copiar y pegar.
        """
        
        return await self.generate_text(prompt)
    
    async def chat(self, message: str, conversation_history: list = None) -> str:
        """Chat conversacional con memoria"""
        if conversation_history is None:
            conversation_history = []
        
        messages = [
            {
                "role": "system",
                "content": "Eres IA Daily Bot, un asistente experto en Inteligencia Artificial. Respondes en español de forma amigable y útil."
            }
        ]
        
        # Añadir historial
        messages.extend(conversation_history[-10:])  # Últimos 10 mensajes
        
        # Añadir mensaje actual
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": {"messages": messages},
            "parameters": {
                "max_tokens": 500,
                "temperature": 0.7
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Usar endpoint internacional
                url = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("output", {}).get("text", "")
                    else:
                        return "❌ Error al procesar tu mensaje"
                        
        except Exception as e:
            return f"❌ Error: {e}"


def load_qwen_config() -> dict:
    """Cargar configuración de Qwen"""
    if QWEN_CONFIG_FILE.exists():
        with open(QWEN_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Config por defecto
    return {
        "api_key": "",
        "enabled": False,
        "model": "qwen-turbo",
        "owner_only": True  # Solo owner puede usar
    }


def save_qwen_config(config: dict):
    """Guardar configuración de Qwen"""
    with open(QWEN_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_qwen_client() -> QwenAI:
    """Obtener cliente de Qwen configurado"""
    config = load_qwen_config()
    
    if not config.get("enabled") or not config.get("api_key"):
        return None
    
    return QwenAI(api_key=config["api_key"])
