#!/usr/bin/env python3
"""
⏰ Termux Alarm Trigger
Ejecuta publicaciones usando alarmas de Termux
"""

import os
import sys
from pathlib import Path

# Añadir path base
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from scheduler import Scheduler
import asyncio


def main():
    """Ejecutar post cuando se activa la alarma"""
    print("🔔 Trigger de alarma activado!")
    
    scheduler = Scheduler()
    
    # Publicar contenido
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scheduler.auto_post())
    
    print("✅ Post publicado desde trigger de alarma")


if __name__ == '__main__':
    main()
