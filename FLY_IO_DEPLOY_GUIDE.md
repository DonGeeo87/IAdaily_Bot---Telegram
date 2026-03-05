# 🤖 IA Daily Bot - Deploy en fly.io

Guía completa para desplegar tu bot de Telegram en fly.io y hacerlo funcionar 24/7 sin depender de tu móvil.

---

## 📋 Índice

1. [Requisitos Previos](#-requisitos-previos)
2. [Preparar el Proyecto](#-preparar-el-proyecto)
3. [Configurar fly.io](#-configurar-flyio)
4. [Deploy Paso a Paso](#-deploy-paso-a-paso)
5. [Verificación y Monitoreo](#-verificación-y-monitoreo)
6. [Solución de Problemas](#-solución-de-problemas)
7. [Costos y Límites](#-costos-y-límites)

---

## 🛠️ Requisitos Previos

### 1. Tener cuenta en fly.io

- Ve a [fly.io](https://fly.io) y regístrate (puedes usar tu cuenta de GitHub)
- Necesitas agregar un método de pago (tarjeta) aunque el free tier es gratuito

### 2. Instalar flyctl (CLI de fly.io)

**Windows (PowerShell o CMD):**
```powershell
winget install fly.flyctl
```

**Mac (Homebrew):**
```bash
brew install flyctl
```

**Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### 3. Tener tu bot de Telegram listo

- Bot creado con @BotFather
- Token del bot
- Canal creado con el bot como administrador

---

## 📁 Preparar el Proyecto

### Archivos incluidos para fly.io

Este proyecto ya incluye todos los archivos necesarios:

| Archivo | Propósito |
|---------|-----------|
| `Dockerfile` | Empaqueta el bot en un contenedor |
| `fly.toml` | Configuración para fly.io |
| `requirements.txt` | Dependencias de Python |
| `config_loader.py` | Carga configuración desde variables de entorno |
| `deploy_fly.sh` | Script automático de deploy |

### 1. Subir código a GitHub

```bash
# En tu carpeta del proyecto
cd C:\GeeoDev\telegram-ia-bot-backup

# Inicializar git (si no lo has hecho)
git init

# Añadir todos los archivos
git add .

# Crear primer commit
git commit -m "🚀 IA Daily Bot - Ready for fly.io"

# Añadir tu repositorio remoto (reemplaza con tu URL)
git remote add origin https://github.com/DonGeeo87/IAdaily_Bot---Telegram.git

# Subir código
git push -u origin main
```

### 2. Verificar que .gitignore esté correcto

El archivo `.gitignore` ya incluido protege tu información sensible:
- ✅ No sube `logs/`
- ✅ No sube `posts/`
- ✅ No sube `.env`
- ✅ No sube configuraciones locales

---

## 🔧 Configurar fly.io

### 1. Iniciar sesión en flyctl

```bash
fly auth login
```

Se abrirá una ventana en tu navegador. Inicia sesión con GitHub.

### 2. Editar fly.toml

Abre el archivo `fly.toml` y cambia:

```toml
app = "iadaily-bot-unico"  # ¡Debe ser único globalmente!
```

**Importante:** El nombre debe ser único en todo fly.io. Si `iadaily-bot` ya existe, usa otro nombre.

### 3. Configurar región

En `fly.toml`, cambia la región si lo prefieres:

```toml
primary_region = "mad"  # Madrid (Europa)
# Otras opciones: "mia" (Miami), "bog" (Bogotá), "gru" (São Paulo)
```

---

## 🚀 Deploy Paso a Paso

### Método 1: Script Automático (Recomendado)

```bash
# Ejecutar script de deploy
bash deploy_fly.sh
```

El script:
1. ✅ Verifica flyctl instalado
2. ✅ Verifica sesión activa
3. ✅ Crea la app si no existe
4. ✅ Configura secrets (te pedirá el token)
5. ✅ Hace deploy
6. ✅ Muestra logs

### Método 2: Deploy Manual

#### Paso 1: Crear la aplicación

```bash
fly launch --no-deploy --region mad --name iadaily-bot-unico
```

#### Paso 2: Configurar secrets (variables sensibles)

```bash
# Token de Telegram
fly secrets set TELEGRAM_BOT_TOKEN="8627686733:AAGgyqXtPu1juP1hjGZbb0iIhJWhq2WN324"

# Canal
fly secrets set TELEGRAM_CHANNEL_ID="@IADailyChannel"

# Admin users (separados por coma si hay múltiples)
fly secrets set TELEGRAM_ADMIN_USERS="2036304183"
```

#### Paso 3: Deploy

```bash
fly deploy --remote-only
```

#### Paso 4: Verificar

```bash
# Estado de la app
fly status

# Ver logs
fly logs --max 50
```

---

## 📊 Verificación y Monitoreo

### Comandos útiles

```bash
# Ver estado
fly status

# Ver logs en tiempo real
fly logs

# Ver logs de las últimas 100 líneas
fly logs --max 100

# Acceder a consola SSH (para debugging)
fly ssh console

# Reiniciar la app
fly restart

# Ver información de la app
fly info

# Ver eventos
fly events
```

### Probar que el bot funciona

1. Abre Telegram
2. Busca tu bot: `@IADaily_Bot` (o el username que elegiste)
3. Envía `/start`
4. Debería responder inmediatamente

### Monitoreo de recursos

```bash
# Uso de CPU/RAM
fly ssh console --command "top"

# Espacio en disco
fly ssh console --command "df -h"
```

---

## ⚠️ Solución de Problemas

### Error: "App name already taken"

**Solución:** Cambia el nombre en `fly.toml`:
```toml
app = "iadaily-bot-otro-nombre"
```

### Error: "No valid token found"

**Solución:** Vuelve a iniciar sesión:
```bash
fly auth logout
fly auth login
```

### Error: "Not authenticated"

**Solución:**
```bash
fly auth login
```

### El bot no responde

1. **Verifica logs:**
   ```bash
   fly logs
   ```

2. **Verifica secrets:**
   ```bash
   fly secrets list
   ```

3. **Reinicia la app:**
   ```bash
   fly restart
   ```

4. **Verifica que el token es correcto:**
   - El token debe ser como: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### Error de configuración

```bash
# Ver variables de entorno
fly ssh console --command "env | grep TELEGRAM"
```

### El bot se cae constantemente

Revisa los logs para ver el error:
```bash
fly logs | grep -i error
```

Posibles causas:
- ❌ Token inválido
- ❌ Canal no existe o el bot no es admin
- ❌ Falta memoria (aumenta en `fly.toml`)

---

## 💰 Costos y Límites

### Free Tier de fly.io

fly.io ofrece un free tier generoso:

| Recurso | Límite Free |
|---------|-------------|
| CPU compartida | Hasta 3 VMs |
| Memoria | 256 MB por VM |
| Ancho de banda | 160 GB/mes |
| Almacenamiento | 3 GB |

### Estimación para este bot

Tu bot debería entrar **completamente en el free tier**:

- **CPU:** ~1-5% (muy bajo)
- **Memoria:** ~50-100 MB
- **Ancho de banda:** ~1-2 GB/mes
- **Costo estimado:** $0/mes ✅

### Monitorear uso

```bash
# Ver uso actual
fly status

# Ver métricas detalladas
fly metrics
```

### Si excedes el free tier

fly.io te notifica antes de cobrar. Para reducir costos:

1. Reduce memoria en `fly.toml`:
   ```toml
   [vm]
   memory_mb = 256
   ```

2. Reduce instancias:
   ```bash
   fly scale count 1
   ```

---

## 🔄 Actualizar el Bot

### Hacer cambios y deploy

```bash
# 1. Hacer cambios en el código
# (edita los archivos que necesites)

# 2. Commit
git add .
git commit -m "✨ Nueva feature: XYZ"

# 3. Push a GitHub
git push

# 4. Deploy a fly.io
fly deploy --remote-only
```

### Rollback (volver a versión anterior)

```bash
# Ver historial de releases
fly releases list

# Volver a una versión específica
fly releases rollback v123
```

---

## 📁 Estructura del Proyecto

```
telegram-ia-bot/
├── Dockerfile              # Configuración Docker
├── fly.toml                # Configuración fly.io
├── requirements.txt        # Dependencias Python
├── config_loader.py        # Carga config desde env
├── deploy_fly.sh           # Script de deploy
├── .gitignore              # Archivos ignorados por git
├── .env.example            # Ejemplo de variables
├── bot_robusto.py          # Bot principal
├── master_scheduler.py     # Scheduler de posts
├── content_generator.py    # Generador de contenido
├── config.json             # Configuración local
└── ... (otros scripts)
```

---

## 🎯 Próximos Pasos

### 1. Configurar dominio personalizado (opcional)

```bash
fly certs add iadaily.tudominio.com
```

### 2. Configurar backups automáticos

Usa un volumen persistente para guardar logs y posts:

```bash
# Crear volumen
fly volumes create iadaily_data --size 1

# Descomentar en fly.toml:
# [[mounts]]
#   source = "iadaily_data"
#   destination = "/app"
```

### 3. Configurar alertas

Recibe emails cuando el bot tenga problemas:

```bash
fly console --command "curl https://hc-ping.com/TU_WEBHOOK"
```

---

## 📞 Soporte

### Documentación oficial

- [fly.io Docs](https://fly.io/docs/)
- [fly.toml reference](https://fly.io/docs/reference/configuration/)
- [flyctl commands](https://fly.io/docs/flyctl/)

### Comunidad

- [fly.io Community](https://community.fly.io/)
- [GitHub Discussions](https://github.com/superfly/flyctl/discussions)

---

## ✅ Checklist Final

- [ ] flyctl instalado
- [ ] Sesión iniciada en fly.io
- [ ] Código subido a GitHub
- [ ] `fly.toml` configurado con nombre único
- [ ] Secrets configurados (TOKEN, CHANNEL_ID, ADMIN_USERS)
- [ ] Deploy completado exitosamente
- [ ] Bot responde a `/start`
- [ ] Logs se ven correctamente
- [ ] Monitoreo configurado

---

**¡Listo! Tu bot ahora funciona 24/7 en fly.io 🚀**

Sin necesidad de tener Termux abierto en tu móvil.
