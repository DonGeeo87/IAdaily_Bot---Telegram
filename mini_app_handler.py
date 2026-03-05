#!/usr/bin/env python3
"""
🎮 Mini App Game Handler - IA Clicker Empire
Maneja la integración de la Mini App en el bot
"""

import os
import json
import logging
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

logger = logging.getLogger(__name__)

# URL de la Mini App (cambiar en producción)
# En desarrollo: http://localhost:3000
# En producción: https://tu-dominio.vercel.app
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://ia-clicker-empire.vercel.app")
BACKEND_URL = os.getenv("BACKEND_URL", "https://ia-clicker-api.fly.dev")


async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /juego - Abre la Mini App"""
    user = update.effective_user
    
    # Crear botón para abrir Mini App
    keyboard = [[
        InlineKeyboardButton(
            "🎮 Jugar Ahora",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )
    ]]
    
    # Si es callback (desde menú), editar mensaje
    if update.callback_query:
        await update.callback_query.edit_message_text(
            f"🎮 **¡IA Clicker Empire!**\n\n"
            f"👋 ¡Hola {user.first_name}!\n\n"
            f"🤖 Construye tu imperio de Inteligencia Artificial\n"
            f"💰 Gana coins tocando el robot\n"
            f"🏪 Compra mejoras y compite en el ranking\n\n"
            f"¡Haz clic en el botón para jugar! 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"🎮 **¡IA Clicker Empire!**\n\n"
            f"👋 ¡Hola {user.first_name}!\n\n"
            f"🤖 Construye tu imperio de Inteligencia Artificial\n"
            f"💰 Gana coins tocando el robot\n"
            f"🏪 Compra mejoras y compite en el ranking\n\n"
            f"¡Haz clic en el botón para jugar! 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    logger.info(f"Usuario {user.id} abrió la Mini App")


async def trivia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /trivia - Abre trivia diaria"""
    user = update.effective_user
    
    keyboard = [[
        InlineKeyboardButton(
            "🧠 Jugar Trivia",
            web_app=WebAppInfo(url=f"{MINI_APP_URL}/trivia")
        )
    ]]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            f"🧠 **Trivia IA del Día**\n\n"
            f"¡Hola {user.first_name}!\n\n"
            f"Responde 5 preguntas sobre IA y gana:\n"
            f"💰 500-2000 coins\n"
            f"⭐ 50-200 XP\n\n"
            f"¡Buena suerte! 🍀",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"🧠 **Trivia IA del Día**\n\n"
            f"¡Hola {user.first_name}!\n\n"
            f"Responde 5 preguntas sobre IA y gana:\n"
            f"💰 500-2000 coins\n"
            f"⭐ 50-200 XP\n\n"
            f"¡Haz clic para jugar! 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ranking - Muestra el leaderboard"""
    # Por ahora, abrir la Mini App en la sección de ranking
    keyboard = [[
        InlineKeyboardButton(
            "🏆 Ver Ranking",
            web_app=WebAppInfo(url=f"{MINI_APP_URL}/leaderboard")
        )
    ]]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            f"🏆 **Ranking Global**\n\n"
            f"Consulta el leaderboard de jugadores\n"
            f"¡Compite por el primer puesto!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"🏆 **Ranking Global**\n\n"
            f"Consulta el leaderboard de jugadores\n"
            f"¡Compite por el primer puesto!\n\n"
            f"¡Haz clic para ver! 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /perfil - Muestra el perfil del jugador"""
    user = update.effective_user
    
    keyboard = [[
        InlineKeyboardButton(
            "👤 Mi Perfil",
            web_app=WebAppInfo(url=f"{MINI_APP_URL}/profile")
        )
    ]]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            f"👤 **Tu Perfil**\n\n"
            f"Nombre: {user.first_name}\n"
            f"ID: `{user.id}`\n\n"
            f"Revisa tus estadísticas y logros:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"👤 **Tu Perfil**\n\n"
            f"Nombre: {user.first_name}\n"
            f"ID: `{user.id}`\n\n"
            f"Revisa tus estadísticas y logros:\n\n"
            f"👇 Haz clic abajo 👇",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )


def get_handlers():
    """Obtener handlers de la Mini App"""
    return [
        CommandHandler('juego', game_command),
        CommandHandler('game', game_command),
        CommandHandler('trivia', trivia_command),
        CommandHandler('ranking', leaderboard_command),
        CommandHandler('perfil', profile_command),
        CommandHandler('profile', profile_command),
    ]
