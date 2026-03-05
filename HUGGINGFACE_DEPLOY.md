# 🤖 IA Daily Bot - Hugging Face Spaces Deployment

## 🚀 Instrucciones Paso a Paso

### 1. Crear Nuevo Space

1. Ve a: https://huggingface.co/spaces
2. Click en **"Create new Space"**
3. Completa:
   - **Space name:** `ia-daily-bot` (o el que quieras)
   - **License:** MIT
   - **Selecciona:** ✅ **Docker**
   - **Architecture:** x86_64

### 2. Configurar Variables de Entorno

En tu Space, ve a **Settings → Variables → New Variable**

Añade:
```
TELEGRAM_BOT_TOKEN=8627686733:AAGgyqXtPu1juP1hjGZbb0iIhJWhq2WN324
```

### 3. Subir Archivos

Sube TODOS los archivos de tu bot:
```bash
# Desde tu computadora (Git)
git clone https://huggingface.co/spaces/TU_USUARIO/ia-daily-bot
cd ia-daily-bot

# Copia todos los archivos del bot
cp ~/telegram-ia-bot/* .

# Sube todo
git add .
git commit -m "Initial commit - IA Daily Bot"
git push
```

### 4. Verificar Deploy

1. Ve a la pestaña **"App"** de tu Space
2. Debería empezar a construir (Building...)
3. Cuando termine dirá **"Running"**
4. Revisa los logs en **"Logs"**

---

## ⚠️ IMPORTANTE - Hugging Face Spaces FREE

### Limitaciones:
- ❌ **NO es 24/7 real** - Se duerme después de inactividad
- ❌ **Máximo 2 CPU, 16GB RAM** (free tier)
- ❌ **No hay garantía de uptime**

### Para 24/7 Real:
- ✅ **Oracle Cloud Free** (mejor opción)
- ✅ **Railway.app** ($5/mes)
- ✅ **Render.com** (free con limitaciones)
- ✅ **VPS propio**

---

## 🔧 Comandos Útiles

### Ver logs:
```bash
# En la UI de Hugging Face
# Ve a tu Space → Logs
```

### Reiniciar:
```bash
# Settings → Factory Reboot
```

---

## 📊 Estructura de Archivos

```
ia-daily-bot/
├── Dockerfile           # ← IMPORTANTE
├── .dockerignore        # ← IMPORTANTE
├── requirements.txt     # Dependencias
├── bot_robusto.py       # Bot principal
├── config.json          # Configuración
├── qwen_config.json     # API Qwen
└── ... (resto de archivos)
```

---

## 🎯 Después del Deploy

### Verificar que funciona:
1. Ve a tu Telegram
2. Busca @IADaily_Bot
3. Envía `/start`
4. Debería responder

### Si NO responde:
1. Revisa los logs en Hugging Face
2. Verifica que `TELEGRAM_BOT_TOKEN` está configurado
3. Reinicia el Space (Factory Reboot)

---

## 💡 Tips

### Para que no se duerma:
- Usa un servicio como **UptimeRobot** para hacer ping cada 5 min
- O mejor: migra a **Oracle Cloud Free** (24/7 real)

### Monitoreo:
- Revisa logs diariamente
- Configura notificaciones de errores

---

**¡Listo! Tu bot estará corriendo en Hugging Face Spaces** 🚀
