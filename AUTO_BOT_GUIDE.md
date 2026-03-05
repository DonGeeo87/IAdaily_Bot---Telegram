# 🤖 Boteo Automático en Termux - Guía Completa

## ✅ LO QUE SE CONFIGURÓ

Tu bot ahora se **auto-inicia y auto-reinicia** automáticamente.

---

## 📁 ARCHIVOS CREADOS

| Archivo | Función |
|---------|---------|
| `auto-start.sh` | Inicia el bot automáticamente |
| `watchdog.sh` | Monitor y reinicia cada 5 min |
| `~/.termux/boot/start-bot.sh` | Boot al encender teléfono |
| `crontab` | Ejecuta watchdog cada 5 min |

---

## 🔧 CÓMO FUNCIONA

### 1. **Auto-Start (auto-start.sh)**
- Verifica si el bot está corriendo
- Si NO está corriendo, lo inicia
- Si YA está corriendo, no hace nada
- Se ejecuta al abrir Termux

### 2. **Watchdog (watchdog.sh)**
- Se ejecuta cada 5 minutos (vía cron)
- Verifica bot y scheduler
- Si alguno cayó, lo reinicia
- Limpia logs antiguos
- Registra todo en `logs/watchdog.log`

### 3. **Termux Boot (start-bot.sh)**
- Se ejecuta al encender el teléfono
- Adquiere wake lock (no se duerme)
- Ejecuta auto-start
- Inicia watchdog en background

---

## 🚀 COMANDOS DE USO

### Iniciar todo manualmente:
```bash
cd ~/telegram-ia-bot
bash auto-start.sh
```

### Ver logs del watchdog:
```bash
tail -f logs/watchdog.log
```

### Verificar procesos:
```bash
ps aux | grep python
```

### Ver cron jobs:
```bash
crontab -l
```

### Reiniciar bot manualmente:
```bash
pkill -f bot_robusto.py
pkill -f master_scheduler.py
bash auto-start.sh
```

---

## ⚙️ CONFIGURACIÓN ACTUAL

### Cron Job (cada 5 minutos):
```
*/5 * * * * cd ~/telegram-ia-bot && bash watchdog.sh
```

### Boot Script:
```
~/.termux/boot/start-bot.sh
```

### Wake Lock:
✅ Activado en boot (no se duerme)

---

## 📊 FLUJO DE AUTOMATIZACIÓN

```
┌─────────────────────────────────────────┐
│  Encender Teléfono                      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Termux:Boot ejecuta start-bot.sh       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Adquiere Wake Lock (no duerme)         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Ejecuta auto-start.sh                  │
│  - Inicia bot_robusto.py                │
│  - Inicia master_scheduler.py           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Cron ejecuta watchdog.sh cada 5 min    │
│  - Verifica bot                         │
│  - Verifica scheduler                   │
│  - Reinicia si cayó                     │
│  - Limpia logs                          │
└─────────────────────────────────────────┘
```

---

## 🔍 VERIFICAR QUE FUNCIONA

### 1. Verificar procesos:
```bash
ps aux | grep python | grep -v grep
```

Deberías ver:
- `python bot_robusto.py`
- `python master_scheduler.py`

### 2. Verificar cron:
```bash
crontab -l
```

Deberías ver:
```
*/5 * * * * cd ~/telegram-ia-bot && bash watchdog.sh
```

### 3. Ver logs del watchdog:
```bash
cat logs/watchdog.log
```

Deberías ver entradas cada 5 minutos.

---

## ⚠️ IMPORTANTE - MANTENER TERMUX ACTIVO

### Para que NO se cierre:

1. **No cerrar Termux** (solo minimizar)
2. **Bloquear en recientes:**
   - Abre apps recientes
   - Toca ícono de Termux
   - Toca candado 🔒

3. **Desactivar optimización de batería:**
   - Ajustes → Apps → Termux
   - Batería → Sin restricciones

4. **Wake lock automático:**
   - Ya está configurado en boot
   - Verifica con: `termux-wake-lock status`

---

## 🛠️ SOLUCIÓN DE PROBLEMAS

### Problema: "El bot se detiene"

**Verifica:**
```bash
# Ver logs
tail -f logs/watchdog.log

# Ver cron
crontab -l

# Ver wake lock
termux-wake-lock status
```

**Reinicia:**
```bash
bash auto-start.sh
```

### Problema: "Watchdog no se ejecuta"

**Verifica cron:**
```bash
# Ver si cron está corriendo
ps aux | grep crond

# Iniciar cron
crond
```

### Problema: "Termux se cierra"

**Soluciones:**
1. Bloquea Termux en recientes (candado)
2. Desactiva optimización de batería
3. No deslices para cerrar Termux

---

## 📈 MONITOREO REMOTO

### Opción 1: Telegram Notifications

Puedes configurar notificaciones al bot cuando se reinicia:

```bash
# En watchdog.sh, agregar después de reiniciar:
curl -s "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<TU_CHAT_ID>&text=Bot reiniciado"
```

### Opción 2: Logs en la nube

Subir logs a Google Drive o similar:
```bash
# Agregar al final de watchdog.sh
rclone sync logs/ remote:logs/
```

---

## 🎯 CHECKLIST DIARIO

### Mañana:
- [ ] Verificar procesos: `ps aux | grep python`
- [ ] Revisar logs: `cat logs/watchdog.log | tail -20`

### Tarde:
- [ ] Probar bot en Telegram: `/start`
- [ ] Verificar posts en canal

### Noche:
- [ ] Verificar wake lock: `termux-wake-lock status`
- [ ] No cerrar Termux

---

## 💡 TIPS PRO

### 1. Auto-reinicio si usa mucha RAM:
El watchdog ya lo hace automáticamente si usa >50% RAM.

### 2. Notificaciones de error:
Agrega esto a watchdog.sh para recibir Telegram cuando algo falle:
```bash
if [ "$ERROR" = true ]; then
    curl -s "https://api.telegram.org/bot$TOKEN/sendMessage?chat_id=$CHAT_ID&text=⚠️ Error en bot"
fi
```

### 3. Backup automático:
```bash
# Agregar a crontab
0 0 * * * tar -czf ~/backup-$(date +%Y%m%d).tar.gz ~/telegram-ia-bot
```

---

## 🚀 RESUMEN

### ¿Qué hace el sistema?

| Componente | Frecuencia | Función |
|------------|------------|---------|
| **auto-start.sh** | Manual/Boot | Inicia bot |
| **watchdog.sh** | Cada 5 min | Verifica y reinicia |
| **start-bot.sh** | Al boot | Inicia al encender |
| **crond** | Siempre | Ejecuta watchdog |

### ¿Qué pasa si...?

| Escenario | ¿Qué pasa? |
|-----------|------------|
| Cierras Termux | ❌ Se detiene todo |
| Minimizas Termux | ✅ Sigue funcionando |
| Reinicias teléfono | ✅ Inicia automático (con Termux:Boot) |
| Bot se crashea | ✅ Watchdog lo reinicia en 5 min |
| Scheduler se detiene | ✅ Watchdog lo reinicia en 5 min |

---

## ✅ COMANDOS RÁPIDOS

```bash
# Iniciar todo
bash auto-start.sh

# Ver logs
tail -f logs/watchdog.log

# Ver procesos
ps aux | grep python

# Reiniciar bot
pkill -f bot_robusto && bash auto-start.sh

# Ver cron
crontab -l
```

---

**¡Listo! Tu bot ahora es 100% automático en Termux** 🚀

Solo asegúrate de:
1. ✅ No cerrar Termux
2. ✅ Tener wake lock activado
3. ✅ Revisar logs diariamente
