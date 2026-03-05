# 🐳 Docker Deployment Guide

Guía completa para ejecutar tu bot con Docker.

---

## 📋 Requisitos

- Docker Desktop instalado
- Tu bot de Telegram configurado
- Token del bot

---

## 🚀 Inicio Rápido

### Windows (PowerShell)

```powershell
# Ejecutar script automático
.\run_docker.ps1
```

### Windows (CMD)

```cmd
# Construir imagen
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" build -t iadaily-bot .

# Ejecutar contenedor
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" run -d ^
    --name iadaily-bot ^
    --restart unless-stopped ^
    -e TELEGRAM_BOT_TOKEN="TU_TOKEN" ^
    -e TELEGRAM_CHANNEL_ID="@TuCanal" ^
    -e TELEGRAM_ADMIN_USERS="123456789" ^
    -v "%cd%\logs:/app/logs" ^
    -v "%cd%\posts:/app/posts" ^
    iadaily-bot
```

### Linux/Mac

```bash
# Construir
docker build -t iadaily-bot .

# Ejecutar
docker run -d \
    --name iadaily-bot \
    --restart unless-stopped \
    -e TELEGRAM_BOT_TOKEN="TU_TOKEN" \
    -e TELEGRAM_CHANNEL_ID="@TuCanal" \
    -e TELEGRAM_ADMIN_USERS="123456789" \
    -v $(pwd)/logs:/app/logs \
    -v $(pwd)/posts:/app/posts \
    iadaily-bot
```

---

## 📊 Docker Compose (Múltiples Servicios)

### Ejecutar todos los servicios

```bash
docker-compose up -d
```

### Servicios disponibles

| Servicio | Descripción |
|----------|-------------|
| `bot` | Bot principal de comandos |
| `scheduler` | Publicación automática |
| `content` | Generador de contenido |

### Ver logs

```bash
# Todos los logs
docker-compose logs -f

# Solo bot
docker-compose logs -f bot

# Solo scheduler
docker-compose logs -f scheduler
```

### Detener

```bash
docker-compose down
```

---

## 🔧 Comandos Útiles

### Ver estado

```bash
docker ps --filter "name=iadaily"
```

### Ver logs

```bash
docker logs iadaily-bot
docker logs -f iadaily-bot  # En tiempo real
docker logs --tail 50 iadaily-bot  # Últimas 50 líneas
```

### Reiniciar

```bash
docker restart iadaily-bot
```

### Detener

```bash
docker stop iadaily-bot
```

### Eliminar

```bash
docker rm -f iadaily-bot
```

### Ver logs de scheduler

```bash
docker logs iadaily-scheduler
```

---

## 📁 Volúmenes Persistentes

Los volúmenes montan directorios locales en el contenedor:

| Local | Contenedor | Descripción |
|-------|------------|-------------|
| `./logs` | `/app/logs` | Logs del bot |
| `./posts` | `/app/posts` | Posts generados |
| `./campaign` | `/app/campaign` | Campañas |

---

## 🔐 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Token de tu bot | `123456:ABC-DEF1234...` |
| `TELEGRAM_CHANNEL_ID` | ID del canal | `@IADailyChannel` |
| `TELEGRAM_ADMIN_USERS` | IDs de admins | `123456789,987654321` |
| `TIMEZONE` | Zona horaria | `America/Mexico_City` |
| `LOG_LEVEL` | Nivel de logs | `INFO`, `DEBUG` |

---

## 🐛 Solución de Problemas

### El contenedor no inicia

```bash
# Ver logs de error
docker logs iadaily-bot

# Verificar token
docker inspect iadaily-bot | grep TELEGRAM
```

### Error de credenciales Docker

```bash
# En Windows, reinicia Docker Desktop
# O ejecuta:
docker logout
docker login
```

### Bot no responde

1. Verifica logs: `docker logs iadaily-bot`
2. Verifica token: debe ser válido
3. Verifica canal: el bot debe ser admin

### Memoria llena

```bash
# Limpiar contenedores viejos
docker system prune -a

# Ver uso de disco
docker system df
```

---

## 🔄 Actualizar Bot

```bash
# 1. Detener contenedor
docker stop iadaily-bot
docker rm iadaily-bot

# 2. Pull de cambios (si usas git)
git pull

# 3. Reconstruir imagen
docker build -t iadaily-bot .

# 4. Iniciar nuevo contenedor
docker run -d --name iadaily-bot ... (mismos parámetros)
```

---

## 📊 Monitoreo

### Uso de recursos

```bash
docker stats iadaily-bot
```

### Logs en tiempo real

```bash
docker logs -f iadaily-bot
```

### Acceder a consola del contenedor

```bash
docker exec -it iadaily-bot bash
```

---

## 🎯 Producción

### Recomendaciones

1. **Restart policy**: `--restart unless-stopped`
2. **Logs rotation**: Configurar en Docker daemon
3. **Health checks**: Habilitar en Dockerfile
4. **Resource limits**: Limitar CPU/RAM si es necesario

### Ejemplo con límites

```bash
docker run -d \
    --name iadaily-bot \
    --restart unless-stopped \
    --memory 512m \
    --cpus 1.0 \
    -e TELEGRAM_BOT_TOKEN="..." \
    iadaily-bot
```

---

## 📚 Más Información

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [fly.io Guide](FLY_IO_DEPLOY_GUIDE.md)

---

**¡Tu bot ahora corre en Docker! 🎉**
