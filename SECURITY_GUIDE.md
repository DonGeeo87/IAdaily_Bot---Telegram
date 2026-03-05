# 🔐 Guía de Seguridad del Bot

## 📋 Sistema de Permisos

El bot tiene un sistema de seguridad con **5 niveles de acceso** para controlar quién puede usar cada función.

---

## 🎯 Niveles de Acceso

| Nivel | Rol | Permisos |
|-------|-----|----------|
| **100** | 👑 Owner | Acceso TOTAL a todos los comandos |
| **50** | 🔧 Admin | Comandos de administración, configuración |
| **20** | ⭐ Premium | Campañas de promoción, posts avanzados |
| **10** | 👤 User | Comandos básicos (generar, noticias, prompts) |
| **0** | ⛔ Banned | SIN ACCESO - Usuario bloqueado |

---

## 🚀 Comandos por Nivel

### 🟢 Nivel 10 - User (Básico - Todos pueden usar)
```
/start - Iniciar bot
/help - Ayuda
/generar - Generar contenido IA
/noticias - Noticias de IA
/prompts - Prompts de ChatGPT
/stats - Estadísticas
/ia [tema] - Consulta en grupos
```

### 🟡 Nivel 20 - Premium
```
Todo lo anterior +
/campana - Campaña de promoción
/post [tema] - Crear post personalizado
/imagen - Generar imágenes (si está configurado)
```

### 🟠 Nivel 50 - Admin
```
Todo lo anterior +
/admin - Panel de administrador
/setup - Configurar APIs
/setgnews [key] - Configurar GNews
/sethf [token] - Configurar HuggingFace
/setpexels [key] - Configurar Pexels
/users - Ver usuarios
/log - Ver logs de acceso
```

### 🔴 Nivel 100 - Owner (Solo tú)
```
Todo lo anterior +
/security - Configuración de seguridad
/grant [user] [rol] - Dar permisos
/revoke [user] [rol] - Quitar permisos
/ban [user] - Banear usuario
/unban [user] - Desbanear
```

---

## ⚙️ Configuración Inicial

### 1. El primer usuario es automáticamente OWNER

Cuando ejecutas el bot por primera vez y envías `/start`, tu usuario queda registrado como **OWNER**.

### 2. Verifica tu rol

```
/start
```

El bot te mostrará tu rol y tu ID de usuario.

### 3. Anota tu ID de usuario

Lo necesitarás para dar permisos a otros.

---

## 🔧 Comandos de Seguridad

### Ver configuración de seguridad (Solo Owner)
```
/security
```

Muestra:
- Owner ID
- Número de admins, premium, baneados
- Logs de acceso

---

### Dar permisos (Solo Owner)

**Dar rol ADMIN:**
```
/grant 123456789 admin
```

**Dar rol PREMIUM:**
```
/grant 123456789 premium
```

**Dar rol OWNER:**
```
/grant 987654321 owner
```

---

### Quitar permisos (Solo Owner)

**Quitar ADMIN:**
```
/revoke 123456789 admin
```

**Quitar PREMIUM:**
```
/revoke 123456789 premium
```

---

### Banear usuario (Solo Owner)
```
/ban 123456789
```

El usuario baneado no podrá usar ningún comando del bot.

---

### Desbanear usuario (Solo Owner)
```
/unban 123456789
```

---

### Ver todos los usuarios (Admin+)
```
/users
```

Muestra:
- Owner
- Admins
- Premium users
- Banned users

---

### Ver logs de acceso (Admin+)
```
/log 50
```

Muestra los últimos 50 accesos al bot (con ✅ o ⛔).

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Dar acceso premium a un amigo

1. Tu amigo usa el bot por primera vez
2. Obtén su ID (con `/users` o pídeselo)
3. Ejecuta: `/grant 123456789 premium`
4. ¡Listo! Ahora puede usar `/campana`

### Ejemplo 2: Banear usuario spammer

1. Ves logs de acceso sospechosos
2. Obtén el ID del usuario
3. Ejecuta: `/ban 123456789`
4. El usuario ya no puede usar el bot

### Ejemplo 3: Hacer admin a tu asistente

1. Obtén el ID de tu asistente
2. Ejecuta: `/grant 987654321 admin`
3. Ahora puede configurar APIs y ver logs

---

## 🛡️ Escenarios Recomendados

### Bot Personal (Solo tú)
- No necesitas configurar nada
- Solo tú tienes acceso (eres el owner)
- Los demás usuarios tienen acceso básico (nivel 10)

### Bot con Equipo
```
# Tú eres Owner
/security  # Verifica que eres owner

# Dar admin a tu socio
/grant 111222333 admin

# Dar premium a tu asistente
/grant 444555666 premium
```

### Bot Público (Cualquiera puede usar)
- Deja los comandos básicos en nivel 10
- Premium en nivel 20 para funciones avanzadas
- Considera requerir aprobación para premium

---

## 📁 Archivos de Seguridad

| Archivo | Función |
|---------|---------|
| `security.json` | Guarda usuarios, roles, logs |
| `security_manager.py` | Lógica de seguridad |
| `logs/bot_*.log` | Logs de actividad |

---

## 🔍 Ver Logs Manualmente

```bash
# Ver últimos logs
tail -f logs/bot_*.log

# Ver logs de seguridad
cat security.json | python -m json.tool
```

---

## ⚠️ Importante

1. **Nunca compartas tu bot token**
2. **Solo da rol ADMIN a personas de confianza**
3. **Revisa los logs regularmente**
4. **El OWNER tiene control total del bot**

---

## 🚨 Si algo sale mal

### Perdiste acceso como Owner:
```bash
# Editar manualmente security.json
nano ~/telegram-ia-bot/security.json

# Asegúrate de que "owner_id" sea tu ID
```

### Usuario baneado por error:
```
/unban 123456789
```

### Ver todos los permisos:
```
/security
/users
```

---

## 📊 Matriz de Permisos Completa

| Comando | Owner | Admin | Premium | User | Banned |
|---------|-------|-------|---------|------|--------|
| /start | ✅ | ✅ | ✅ | ✅ | ❌ |
| /generar | ✅ | ✅ | ✅ | ✅ | ❌ |
| /noticias | ✅ | ✅ | ✅ | ✅ | ❌ |
| /prompts | ✅ | ✅ | ✅ | ✅ | ❌ |
| /stats | ✅ | ✅ | ✅ | ✅ | ❌ |
| /campana | ✅ | ✅ | ✅ | ❌ | ❌ |
| /post | ✅ | ✅ | ✅ | ❌ | ❌ |
| /setup | ✅ | ✅ | ❌ | ❌ | ❌ |
| /setgnews | ✅ | ✅ | ❌ | ❌ | ❌ |
| /users | ✅ | ✅ | ❌ | ❌ | ❌ |
| /log | ✅ | ✅ | ❌ | ❌ | ❌ |
| /security | ✅ | ❌ | ❌ | ❌ | ❌ |
| /grant | ✅ | ❌ | ❌ | ❌ | ❌ |
| /ban | ✅ | ❌ | ❌ | ❌ | ❌ |

---

**¡Configura bien los permisos para mantener tu bot seguro!** 🔐
