#!/usr/bin/env python3
"""
🎯 Engagement Bot - Sistema de participación e interacción diaria
Encuestas, quizzes, desafíos para mantener la comunidad activa
"""

import os
import json
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path

try:
    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputPollOption
    from telegram.ext import Application, CommandHandler, ContextTypes, PollAnswerHandler
except ImportError:
    print("Instalando python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputPollOption
    from telegram.ext import Application, CommandHandler, ContextTypes, PollAnswerHandler

# Paths
BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
LOGS_DIR = BASE_DIR / "logs"
ENGAGEMENT_FILE = BASE_DIR / "engagement_config.json"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOGS_DIR / f"engagement_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EngagementBot:
    """Sistema de engagement y participación"""
    
    def __init__(self):
        self.config = self.load_config()
        self.token = self.config["telegram"]["bot_token"]
        self.channel = self.config["telegram"]["channel_id"]
        self.bot = Bot(token=self.token)
        
        # Encuestas predefinidas
        self.polls = [
            {
                "question": "¿Qué herramienta de IA usas más?",
                "options": ["ChatGPT", "Claude", "Gemini", "Otra"],
                "correct_answer": None  # Sin respuesta correcta (encuesta normal)
            },
            {
                "question": "¿Para qué usas IA principalmente?",
                "options": ["Trabajo", "Estudio", "Proyectos personales", "Curiosidad"],
                "correct_answer": None
            },
            {
                "question": "¿Qué tipo de contenido prefieres?",
                "options": ["Herramientas", "Noticias", "Tutoriales", "Prompts"],
                "correct_answer": None
            },
            {
                "question": "¿Cuánto tiempo dedicas a IA por día?",
                "options": ["< 30 min", "30-60 min", "1-2 horas", "+2 horas"],
                "correct_answer": None
            },
            {
                "question": "¿Qué modelo de Qwen prefieres?",
                "options": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-vl"],
                "correct_answer": None
            }
        ]
        
        # Quizzes de IA
        self.quizzes = [
            {
                "question": "🧠 ¿Qué significa GPT en ChatGPT?",
                "options": ["General Pre-trained Transformer", "Generative Pre-trained Transformer", "Global Processing Tool", "Generic Pattern Tracker"],
                "correct": 1,  # Índice de respuesta correcta
                "explicacion": "GPT = Generative Pre-trained Transformer. Es un modelo de lenguaje entrenado para generar texto."
            },
            {
                "question": "🤖 ¿Qué empresa creó Claude?",
                "options": ["OpenAI", "Google", "Anthropic", "Meta"],
                "correct": 2,
                "explicacion": "Claude fue creado por Anthropic, una startup fundada por ex-empleados de OpenAI."
            },
            {
                "question": "💡 ¿Qué es un 'prompt'?",
                "options": ["Un error de IA", "Una instrucción para la IA", "Un tipo de modelo", "Una herramienta"],
                "correct": 1,
                "explicacion": "Un prompt es la instrucción o pregunta que le damos a la IA para obtener una respuesta."
            },
            {
                "question": "🎨 ¿Qué IA es mejor para generar imágenes?",
                "options": ["ChatGPT", "Midjourney", "Claude", "Perplexity"],
                "correct": 1,
                "explicacion": "Midjourney es especializado en generación de imágenes artísticas de alta calidad."
            },
            {
                "question": "📊 ¿Qué es el 'fine-tuning'?",
                "options": ["Ajustar parámetros", "Entrenar un modelo base para tarea específica", "Corregir errores", "Optimizar velocidad"],
                "correct": 1,
                "explicacion": "Fine-tuning es entrenar un modelo pre-entrenado para una tarea específica con datos especializados."
            }
        ]
        
        # Desafíos diarios
        self.challenges = [
            {
                "titulo": "🎯 Desafío del Día: Prompt Engineering",
                "descripcion": "Crea el mejor prompt para que ChatGPT te ayude a planificar tu semana. Comparte tu prompt en los comentarios.",
                "recompensa": "🏆 Featured + Review de tu prompt"
            },
            {
                "titulo": "🛠️ Desafío del Día: Herramienta Nueva",
                "descripcion": "Prueba una herramienta de IA que nunca hayas usado y comparte tu experiencia en 3 líneas.",
                "recompensa": "🏆 Mención en el canal"
            },
            {
                "titulo": "💡 Desafío del Día: Caso de Uso",
                "descripcion": "Cuéntanos cómo usaste IA esta semana para ahorrar tiempo. Sé específico con el antes/después.",
                "recompensa": "🏆 Caso destacado"
            },
            {
                "titulo": "🎨 Desafío del Día: Creación con IA",
                "descripcion": "Crea algo (imagen, texto, código) usando IA y compártelo. Vale cualquier cosa!",
                "recompensa": "🏆 Galería de la comunidad"
            },
            {
                "titulo": "📚 Desafío del Día: Aprendizaje",
                "descripcion": "Aprende una función nueva de tu IA favorita y enséñala en los comentarios.",
                "recompensa": "🏆 Reconocimiento de experto"
            }
        ]
    
    def load_config(self) -> dict:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def post_daily_poll(self, context: ContextTypes.DEFAULT_TYPE):
        """Publicar encuesta diaria"""
        poll_data = random.choice(self.polls)
        
        chat_id = self.channel
        
        try:
            await self.bot.send_poll(
                chat_id=chat_id,
                question=poll_data["question"],
                options=poll_data["options"],
                is_anonymous=True,
                type="regular",
                allows_multiple_answers=False
            )
            logger.info("✅ Encuesta diaria publicada")
        except Exception as e:
            logger.error(f"❌ Error al publicar encuesta: {e}")
    
    async def post_weekly_quiz(self, context: ContextTypes.DEFAULT_TYPE):
        """Publicar quiz semanal con respuesta correcta"""
        quiz_data = random.choice(self.quizzes)
        
        chat_id = self.channel
        
        try:
            await self.bot.send_poll(
                chat_id=chat_id,
                question=quiz_data["question"],
                options=quiz_data["options"],
                is_anonymous=False,
                type="quiz",
                correct_option=quiz_data["correct"],
                explanation=quiz_data["explicacion"]
            )
            logger.info("✅ Quiz semanal publicado")
        except Exception as e:
            logger.error(f"❌ Error al publicar quiz: {e}")
    
    async def post_daily_challenge(self, context: ContextTypes.DEFAULT_TYPE):
        """Publicar desafío del día"""
        challenge = random.choice(self.challenges)
        
        chat_id = self.channel
        
        message = f"""
{challenge["titulo"]}

{challenge["descripcion"]}

🎁 **Recompensa:** {challenge["recompensa"]}

👇 **Participa:**
1. Completa el desafío
2. Comenta tu resultado
3. Inspira a otros miembros

¡Esperamos ver tu participación! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("📢 Compartir Desafío", url=f"https://t.me/share/url?url=https://t.me/{self.channel.replace('@', '')}")]
        ]
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            logger.info("✅ Desafío diario publicado")
        except Exception as e:
            logger.error(f"❌ Error al publicar desafío: {e}")
    
    async def post_engagement_question(self, context: ContextTypes.DEFAULT_TYPE):
        """Publicar pregunta de engagement para generar comentarios"""
        questions = [
            "💬 ¿Qué herramienta de IA descubriste esta semana que te voló la cabeza?",
            "🤔 Si pudieras pedirle una función nueva a ChatGPT, ¿qué le pedirías?",
            "🎯 ¿Cuál fue tu mejor uso de IA esta semana? ¡Comparte!",
            "⚡ ¿Qué tarea repetitiva te gustaría automatizar con IA?",
            "🚀 ¿Qué proyecto personal tienes que podría mejorarse con IA?",
            "💡 ¿Qué prompt te funcionó tan bien que lo usas siempre?",
            "📊 ¿Qué métrica de productividad mejoraste usando IA?",
            "🎨 ¿Qué has creado con IA de lo que te sientes orgulloso?"
        ]
        
        question = random.choice(questions)
        
        chat_id = self.channel
        
        keyboard = [
            [InlineKeyboardButton("💬 Responder", url=f"https://t.me/{self.channel.replace('@', '')}")]
        ]
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=f"{question}\n\n👇 **Te leemos en los comentarios!**",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            logger.info("✅ Pregunta de engagement publicada")
        except Exception as e:
            logger.error(f"❌ Error al publicar pregunta: {e}")
    
    def get_schedule(self) -> dict:
        """Obtener horario de engagement"""
        return {
            "poll_daily": "14:00",  # Encuesta diaria
            "quiz_weekly": "18:00",  # Quiz semanal (viernes)
            "challenge_daily": "10:00",  # Desafío diario
            "question_daily": "16:00"  # Pregunta de engagement
        }


def main():
    print("🎯 Engagement Bot listo!")
    print("\n📅 Horario de actividades:")
    bot = EngagementBot()
    schedule = bot.get_schedule()
    for activity, time in schedule.items():
        print(f"   • {activity}: {time}")
    print("\n💡 Las actividades se publicarán automáticamente en el canal.")


if __name__ == '__main__':
    main()
