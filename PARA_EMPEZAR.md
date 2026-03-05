# 🚀 Tu Bot de Telegram 24/7 en fly.io

## ✅ Archivos Creados

He preparado todo lo necesario para deployar tu bot en fly.io:

| Archivo | Propósito |
|---------|-----------|
| `Dockerfile` | Empaqueta el bot en contenedor Docker |
| `fly.toml` | Configuración para fly.io |
| `requirements.txt` | Dependencias de Python |
| `config_loader.py` | Soporte para variables de entorno |
| `deploy_fly.sh` | Script deploy para Linux/Mac |
| `deploy_fly.bat` | Script deploy para Windows |
| `docker-compose.yml` | Para desarrollo local con Docker |
| `.gitignore` | Excluye archivos sensibles |
| `.env.example` | Ejemplo de variables de entorno |
| `FLY_IO_DEPLOY_GUIDE.md` | Guía completa de deploy |
| `DEPLOY_RAPIDO.md` | Pasos rápidos |

---

## 📋 Pasos a Seguir

### 1️⃣ Subir tu código a GitHub

Tu repositorio: https://github.com/DonGeeo87/IAdaily_Bot---Telegram

```bash
cd C:\GeeoDev\telegram-ia-bot-backup

# Inicializar git (si no lo has hecho)
git init

# Añadir todos los archivos
git add .

# Crear commit
git commit -m "🚀 IA Daily Bot - Ready for fly.io deployment"

# Conectar con tu repo (si no está conectado)
git remote add origin https://github.com/DonGeeo87/IAdaily_Bot---Telegram.git

# Subir código
git push -u origin main
```

---

### 2️⃣ Instalar flyctl en Windows

Abre **PowerShell** como administrador:

```powershell
winget install fly.flyctl
```

O descarga desde: https://fly.io/docs/hands-on/install-flyctl/

---

### 3️⃣ Editar fly.toml

Abre `fly.toml` y cambia el nombre de la app:

```toml
app = "iadaily-bot-geeo"  # ⚠️ Debe ser ÚNICO globalmente
```

Ejemplos de nombres únicos:
- `iadaily-bot-geeo`
- `iadaily-bot-telegram-esp`
- `ia-daily-bot-2024`

---

### 4️⃣ Iniciar sesión en fly.io

```bash
fly auth login
```

Se abrirá tu navegador. Inicia sesión con tu cuenta de GitHub.

---

### 5️⃣ Configurar Secrets (variables sensibles)

```bash
# Token de tu bot
fly secrets set TELEGRAM_BOT_TOKEN="8627686733:AAGgyqXtPu1juP1hjGZbb0iIhJWhq2WN324"

# Canal
fly Secrets set TELEGRAM_CHANNEL_ID="@IADailyChannel"

# Admin users
fly secrets set TELEGRAM_ADMIN_USERS="2036304183"
```

---

### 6️⃣ Deploy

**Opción A: Usar script de Windows**
```bash
deploy_fly.bat
```

**Opción B: Manual**
```bash
# Crear la app
fly launch --no-deploy --region mad --name iadaily-bot-geeo

# Deploy
fly deploy --remote-only
```

---

### 7️⃣ Verificar

```bash
# Ver estado
fly status

# Ver logs
fly logs

# Probar el bot en Telegram
# Envía /start a @IADaily_Bot
```

---

## 🎉 ¡Listo!

Tu bot ahora funciona **24/7** en la nube sin necesidad de tener:
- ❌ Termux abierto
- ❌ Tu móvil encendido
- ❌ Consumiendo batería

---

## 📊 Comandos Útiles

```bash
fly status          # Ver estado del bot
fly logs            # Ver logs en tiempo real
fly restart         # Reiniciar el bot
fly ssh console     # Acceder a consola SSH
fly apps list       # Ver tus apps
fly metrics         # Ver métricas de uso
```

---

## 💰 Costo Estimado

**Free Tier de fly.io:**
- ✅ 3 VMs compartidas gratis
- ✅ 160 GB ancho de banda/mes
- ✅ 3 GB almacenamiento

**Tu bot usará:**
- CPU: ~1-5%
- Memoria: ~50-100 MB
- Ancho de banda: ~1-2 GB/mes

**Costo: $0/mes** 🎉

---

## ⚠️ Problemas Comunes

### "App name already taken"
El nombre debe ser único en todo fly.io. Cambia a otro nombre en `fly.toml`.

### "Not authenticated"
Ejecuta: `fly auth login`

### "No valid payment method"
Agrega una tarjeta en: https://fly.io/dashboard

### El bot no responde
```bash
# Ver logs
fly logs

# Reiniciar
fly restart

# Verificar secrets
fly secrets list
```

---

## 📚 Documentación Adicional

- `FLY_IO_DEPLOY_GUIDE.md` - Guía completa y detallada
- `DEPLOY_RAPIDO.md` - Pasos rápidos
- `README.md` - Documentación general del proyecto

---

## 🔗 Enlaces Importantes

- **fly.io Dashboard:** https://fly.io/dashboard
- **Documentación fly.io:** https://fly.io/docs
- **Tu Bot:** https://t.me/IADaily_Bot
- **Tu Canal:** https://t.me/IADailyChannel

---

**¡Éxito con el deploy! 🚀**

Si tienes problemas, revisa los logs con `fly logs` o consulta la guía completa.
