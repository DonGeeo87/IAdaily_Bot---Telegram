#!/usr/bin/env python3
"""
🔋 Battery Trigger
Publica cuando la batería alcanza cierto nivel
"""

import os
import subprocess
from pathlib import Path

def get_battery_level():
    """Obtener nivel de batería desde Termux API"""
    try:
        result = subprocess.run(
            ['termux-battery-status'],
            capture_output=True,
            text=True
        )
        import json
        data = json.loads(result.stdout)
        return data['percentage']
    except:
        return -1


def main():
    level = get_battery_level()
    
    if level == -1:
        print("❌ No se pudo leer la batería")
        return
    
    print(f"🔋 Nivel de batería: {level}%")
    
    # Publicar si la batería está cargada (>80%)
    if level >= 80:
        print("✅ Batería suficiente, publicando...")
        os.system(f"cd {Path(__file__).parent.parent} && python scheduler.py")
    else:
        print("⏭️  Batería baja, esperando...")


if __name__ == '__main__':
    main()
