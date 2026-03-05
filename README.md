# 🤖 IA Daily Bot - Telegram Auto Publisher

Bot automático para publicar contenido sobre Inteligencia Artificial en Telegram.

## 📋 Características

- ✅ **Publicación automática** en horarios configurables
- ✅ **Generador de contenido** sobre IA (herramientas, noticias, tips, recursos)
- ✅ **Scheduler integrado** - publica solo sin intervención
- ✅ **Logs de actividad** - tracking completo
- ✅ **Fácil configuración** - solo necesitas el token de tu bot
- ✅ **Deploy en la nube** - funciona 24/7 sin depender de tu móvil

---

## 🚀 Opciones de Deploy

### Opción 1: fly.io (Recomendada - 24/7 Gratis)

Tu bot funciona en la nube sin necesidad de tener tu móvil encendido.

```bash
# Ver guía completa
cat FLY_IO_DEPLOY_GUIDE.md
```

**Pasos rápidos:**
1. Instala flyctl: `winget install fly.flyctl`
2. `fly auth login`
3. `fly deploy --remote-only`
4. ¡Listo!

✅ **Ventajas:** 24/7 real, gratis en free tier, sin consumir batería de tu móvil

---

### Opción 2: Termux Local (Tu móvil)

Para desarrollo o testing en tu móvil con Termux.

### Paso 1: Crear el Bot en Telegram

1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot`
3. Elige un nombre: `IA Daily`
4. Elige un username: `IADaily_Bot` (o el que hayas conseguido)
5. **Copia el TOKEN** que te da BotFather

### Paso 2: Crear Canal

1. En Telegram, crea un **Nuevo Canal**
2. Nombre: `IA Daily 🤖`
3. Hazlo **PÚBLICO** para obtener un enlace tipo `@IADailyChannel`
4. Añade tu bot como **ADMINISTRADOR** del canal

### Paso 3: Configurar el Bot

```bash
# Ir al directorio del bot
cd ~/telegram-ia-bot

# Ejecutar instalación
bash install.sh
```

### Paso 4: Editar config.json

```bash
# Abrir configuración
nano config.json
```

Reemplaza:
- `"bot_token": "TU_TOKEN_AQUI"` → pega tu token de BotFather
- `"channel_id": "@TU_CANAL_ID"` → pon el ID de tu canal (ej: `@IADailyChannel`)

Guarda con `Ctrl+O` y sal con `Ctrl+X`

## 📁 Estructura

```
telegram-ia-bot/
├── bot.py              # Bot principal (comandos)
├── bot_robusto.py      # Bot robusto con múltiples features
├── master_scheduler.py # Programador automático de posts
├── scheduler.py        # Scheduler básico
├── content_generator.py # Generador de contenido
├── config_loader.py    # Carga config desde variables de entorno
├── config.json         # Configuración
├── requirements.txt    # Dependencias Python
├── Dockerfile          # Configuración Docker
├── fly.toml            # Configuración fly.io
├── docker-compose.yml  # Docker Compose para desarrollo
├── deploy_fly.sh       # Script de deploy a fly.io
├── install.sh          # Script de instalación local
├── .gitignore          # Archivos ignorados por git
├── .env.example        # Ejemplo de variables de entorno
├── posts/              # Posts generados
├── logs/               # Logs de actividad
├── campaign/           # Campañas de promoción
└── triggers/           # Triggers de Termux
```

## 🎯 Uso

### Iniciar el Bot (comandos)

```bash
python bot.py
```

Comandos disponibles en Telegram:
- `/start` - Iniciar
- `/schedule` - Ver horario
- `/status` - Estado (admins)
- `/help` - Ayuda

### Iniciar Scheduler (auto-post)

```bash
python scheduler.py
```

Esto publicará automáticamente a las horas configuradas (por defecto: 08:00, 12:00, 16:00, 20:00)

### Generar Contenido Manualmente

```bash
python content_generator.py
```

## ⏰ Configurar Horarios

Edita `config.json`:

```json
"schedule": {
    "times": ["08:00", "12:00", "16:00", "20:00"]
}
```

## 🔄 Ejecutar en Segundo Plano

### Opción 1: tmux (recomendado)

```bash
# Instalar tmux
pkg install tmux

# Crear sesión
tmux new -s iabot

# Ejecutar scheduler
python scheduler.py

# Salir (Ctrl+B, luego D)
# El bot sigue corriendo

# Volver a la sesión
tmux attach -t iabot
```

### Opción 2: nohup

```bash
nohup python scheduler.py > logs/scheduler.log 2>&1 &
```

### Opción 3: Termux Boot (al iniciar)

```bash
# Instalar Termux:Boot desde F-Droid
mkdir -p ~/.termux/boot
cp scheduler.py ~/.termux/boot/
```

## 📊 Tipos de Contenido

| Hora | Tipo | Emoji |
|------|------|-------|
| 08:00 | Herramienta IA | 🌅 |
| 12:00 | Noticia | ☀️ |
| 16:00 | Tip/Prompt | 🌆 |
| 20:00 | Recurso | 🌙 |

## 🔧 Comandos Útiles

```bash
# Ver logs en tiempo real
tail -f logs/scheduler_*.log

# Ver posts generados
ls -la posts/

# Reiniciar el bot
pkill -f scheduler.py && python scheduler.py

# Ver estado
ps aux | grep python
```

## 💡 Monetización

1. **Afiliados**: Enlaces de herramientas con referral
2. **Premium**: Canal VIP con contenido exclusivo
3. **Promociones**: Publicar herramientas pagas
4. **Donaciones**: Link a Ko-fi/Patreon

## ⚠️ Importante

- **No hagas spam** - Máximo 4-6 posts/día
- **Contenido de valor** - Evita clickbait barato
- **Respeta copyright** - Cita fuentes originales
- **Backup** - Guarda tu config.json en lugar seguro

## 🆘 Soporte

Si tienes problemas:

1. Revisa los logs en `logs/`
2. Verifica que el token es correcto
3. Asegúrate de que el bot es ADMIN del canal
4. Prueba enviar `/start` al bot

## 📄 Licencia

MIT - Úsalo como quieras

---

**Hecho con ❤️ para la comunidad de IA en Telegram**

Canal: @IADaily_Bot
