# 📦 GUÍA DE MIGRACIÓN A LAPTOP

## 🎯 ¿POR QUÉ MIGRAR?

| Móvil (Termux) | Laptop |
|---------------|--------|
| ✅ Portable | ✅ Teclado completo |
| ❌ Pantalla chica | ✅ Múltiples ventanas |
| ❌ Edición limitada | ✅ IDE completo (VS Code) |
| ❌ Recursos limitados | ✅ Más potencia |
| ❌ Debugging difícil | ✅ Herramientas pro |

---

## 📋 ARCHIVOS IMPORTANTES PARA LLEVAR

### 1. **Configuraciones CRÍTICAS** 🔐
```bash
# Copiar estos archivos a un lugar seguro:
~/telegram-ia-bot/config.json          # Token del bot, tu chat_id
~/telegram-ia-bot/apis_config.json     # API key de GNews
~/telegram-ia-bot/security.json        # Usuarios y permisos
~/telegram-ia-bot/qwen_config.json     # Config de Qwen (si existe)
```

### 2. **Código del Bot** 🤖
```bash
~/telegram-ia-bot/bot_robusto.py       # Bot principal
~/telegram-ia-bot/campaign_manager.py  # Generador de campañas
~/telegram-ia-bot/security_manager.py  # Sistema de seguridad
~/telegram-ia-bot/qwen_ai.py           # Integración Qwen
~/telegram-ia-bot/analytics_dashboard.py
~/telegram-ia-bot/growth_tracker.py
~/telegram-ia-bot/welcome_bot.py
~/telegram-ia-bot/engagement_bot.py
```

### 3. **Archivos de Soporte** 📁
```bash
~/telegram-ia-bot/scheduler.py         # Programador de posts
~/telegram-ia-bot/master_scheduler.py
~/telegram-ia-bot/watchdog.sh          # Monitor del bot
~/telegram-ia-bot/start_all.sh         # Scripts de inicio
~/telegram-ia-bot/auto-start.sh
```

### 4. **Directorios de Datos** 📊
```bash
~/telegram-ia-bot/posts/               # Posts generados
~/telegram-ia-bot/campaign/            # Campañas
~/telegram-ia-bot/logs/                # Logs (opcional)
~/telegram-ia-bot/triggers/            # Triggers
~/telegram-ia-bot/social_posts/        # Posts para redes
```

---

## 🚀 MÉTODOS DE MIGRACIÓN

### Opción 1: **Git/GitHub** ⭐ RECOMENDADA

**En el móvil (antes de migrar):**
```bash
cd ~/telegram-ia-bot

# Inicializar repositorio si no existe
git init

# Crear .gitignore para no subir archivos sensibles
cat > .gitignore << EOF
config.json
apis_config.json
security.json
qwen_config.json
*.log
__pycache__/
.env
EOF

# Agregar todo y hacer commit
git add *.py *.sh *.md *.json
git commit -m "Migración inicial del bot"

# Crear repo en GitHub y hacer push
git remote add origin https://github.com/TU_USUARIO/ia-daily-bot.git
git branch -M main
git push -u origin main
```

**En la laptop (después):**
```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/ia-daily-bot.git
cd ia-daily-bot

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o en Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivos de configuración (manualmente o con scp)
# Ver sección "Transferir configs" más abajo
```

---

### Opción 2: **SCP/SFTP** (Directo)

**Desde la laptop:**
```bash
# Crear directorio
mkdir -p ~/projects/ia-daily-bot

# Copiar todo el proyecto (excluyendo logs)
scp -r user@tu-movil:~/telegram-ia-bot/* ~/projects/ia-daily-bot/

# O usar rsync para más control
rsync -av --exclude '*.log' --exclude '__pycache__' \
    user@tu-movil:~/telegram-ia-bot/ \
    ~/projects/ia-daily-bot/
```

---

### Opción 3: **Google Drive / Dropbox** ☁️

**En el móvil:**
```bash
# Crear backup comprimido
cd ~
tar --exclude='telegram-ia-bot/*.log' \
    --exclude='telegram-ia-bot/__pycache__' \
    -czf telegram-ia-bot-backup.tar.gz telegram-ia-bot/

# Subir a Google Drive (usando rclone o app)
# O compartir manualmente desde el administrador de archivos
```

**En la laptop:**
```bash
# Descargar y extraer
tar -xzf telegram-ia-bot-backup.tar.gz
mv telegram-ia-bot ~/projects/ia-daily-bot
```

---

## 🔐 TRANSFERIR ARCHIVOS SENSIBLES

### Método Seguro (Recomendado)

**1. En el móvil, encriptar configs:**
```bash
cd ~/telegram-ia-bot

# Crear archivo encriptado con contraseña
tar czf - config.json apis_config.json security.json | \
    openssl enc -aes-256-cbc -salt -pbkdf2 -out configs-encrypted.tar.gz

# Te pedirá una contraseña - USÁ UNA QUE RECORDÉS
```

**2. Transferir `configs-encrypted.tar.gz`** (por el método que elijas)

**3. En la laptop, desencriptar:**
```bash
openssl enc -aes-256-cbc -d -pbkdf2 \
    -in configs-encrypted.tar.gz | \
    tar xzf -
```

---

## 💻 SETUP EN LAPTOP

### 1. **Instalar Python y dependencias**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

**Windows:**
```powershell
# Descargar Python de python.org
# O usar winget:
winget install Python.Python.3.11
winget install Git.Git
```

**macOS:**
```bash
brew install python3 git
```

### 2. **Configurar entorno**

```bash
cd ~/projects/ia-daily-bot

# Crear entorno virtual
python3 -m venv venv

# Activar (Linux/Mac)
source venv/bin/activate

# Activar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python bot_robusto.py --help  # O el comando que use tu bot
```

### 3. **Configurar IDE (VS Code)**

```bash
# Instalar VS Code
# Ubuntu:
sudo snap install code --classic

# Windows/macOS: Descargar de code.visualstudio.com

# Extensiones recomendadas:
# - Python (Microsoft)
# - Pylance
# - GitLens
# - Docker (si usás Docker)
```

---

## 🔄 MANTENER AMBOS DISPOSITIVOS SYNCEADOS

### Opción A: **Git Flow**

```bash
# En el móvil (antes de terminar sesión):
cd ~/telegram-ia-bot
git add .
git commit -m "Cambios desde móvil"
git push

# En la laptop (al empezar):
cd ~/projects/ia-daily-bot
git pull
```

### Opción B: **Script de Sync Automático**

Crear `~/sync-bot.sh`:
```bash
#!/bin/bash
# Sync entre móvil y laptop vía rsync

MOBIL_IP="192.168.1.XX"  # IP de tu móvil en la misma red
PROJECT_PATH="~/telegram-ia-bot"

# De laptop a móvil
rsync -av --exclude '*.log' ~/projects/ia-daily-bot/ \
    user@$MOBIL_IP:$PROJECT_PATH/

# De móvil a laptop (ejecutar en el móvil)
# rsync -av --exclude '*.log' $PROJECT_PATH/ user@$LAPTOP_IP:~/projects/ia-daily-bot/
```

---

## 🎮 PARA EL JUEGO (QUIZ CHALLENGE)

### Estructura recomendada en laptop:

```
ia-daily-bot/
├── bot/                    # Bot de Telegram existente
│   ├── bot_robusto.py
│   ├── campaign_manager.py
│   └── ...
├── quiz_game/              # NUEVO - Juego
│   ├── backend/
│   │   ├── app.py         # FastAPI
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── questions.py   # 200+ preguntas
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html     # Telegram Web App
│   │   ├── style.css
│   │   └── game.js
│   └── config.json
├── docker-compose.yml      # Para deploy fácil
└── README.md
```

---

## ✅ CHECKLIST DE MIGRACIÓN

### Antes de migrar:
- [ ] Hacer backup de configs
- [ ] Crear repositorio en GitHub
- [ ] Anotar tu chat_id: `2036304183`
- [ ] Anotar token del bot (en config.json)
- [ ] Anotar API key de GNews

### En la laptop:
- [ ] Clonar repositorio
- [ ] Instalar Python 3.10+
- [ ] Crear entorno virtual
- [ ] Instalar dependencias
- [ ] Copiar configs (config.json, apis_config.json, security.json)
- [ ] Probar el bot: `python bot_robusto.py`
- [ ] Configurar VS Code
- [ ] Configurar Git para sync

### Después:
- [ ] Detener bot en el móvil
- [ ] Iniciar bot en laptop
- [ ] Probar comandos en Telegram
- [ ] Verificar scheduler funciona
- [ ] Configurar auto-start (systemd o cron)

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### "No encuentra python-telegram-bot"
```bash
source venv/bin/activate  # Asegurate de activar el venv
pip install -r requirements.txt
```

### "Token inválido"
Verificar que `config.json` se copió correctamente:
```bash
cat config.json | grep bot_token
```

### "Permission denied" en scripts .sh
```bash
chmod +x *.sh
chmod +x watchdog.sh
```

---

## 📞 PRÓXIMOS PASOS

1. **Elegí método de migración** (Git recomendado)
2. **Creá repositorio en GitHub** (privado o público)
3. **Hacé push desde el móvil**
4. **Cloná en la laptop**
5. **Configurá entorno**
6. **Probá el bot**
7. **Empezá con el juego!** 🎮

---

¿Necesitás ayuda con algún paso en particular?
