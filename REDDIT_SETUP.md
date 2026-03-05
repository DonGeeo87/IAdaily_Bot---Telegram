# 🤖 Configuración de Reddit API para IA Daily

## 📋 Paso a Paso (10 minutos)

---

## 1️⃣ Crear Aplicación en Reddit

### Ve a Reddit Apps
👉 https://www.reddit.com/prefs/apps

### Pasos:
1. **Inicia sesión** en tu cuenta de Reddit
2. Baja hasta **"are you a developer? create an app..."**
3. Haz clic en **"create another app"** o **"create an app"**

### Completa el formulario:

| Campo | Valor |
|-------|-------|
| **name** | `IA Daily Bot` |
| **app type** | ✅ **script** (importante!) |
| **description** | `Bot para compartir contenido de IA` |
| **about url** | `https://t.me/IADailyChannel` |
| **redirect uri** | `http://localhost:8080` |

### Después de crear:
Verás algo como esto:

```
IA Daily Bot
a reddit application by /u/TU_USUARIO

client_id: abc123xyz456
client_secret: ABCDEFghijklmnop1234567890
```

**⚠️ IMPORTANTE:**
- El **client_id** es la cadena DEBAJO del nombre (no incluye "Personal use script")
- El **client_secret** está junto a la palabra "secret"

---

## 2️⃣ Configurar el Bot

### Ejecuta por primera vez:

```bash
cd ~/telegram-ia-bot
python reddit_poster.py
```

Esto creará `reddit_config.json` con una plantilla.

### Edita la configuración:

```bash
nano reddit_config.json
```

### Reemplaza con TUS datos:

```json
{
  "credentials": {
    "client_id": "abc123xyz456",
    "client_secret": "ABCDEFghijklmnop1234567890",
    "username": "TU_USUARIO_DE_REDDIT",
    "password": "TU_PASSWORD_DE_REDDIT",
    "user_agent": "IA Daily Bot v1.0 by /u/TU_USUARIO_DE_REDDIT"
  }
}
```

### Guarda:
- `Ctrl + O` → Enter
- `Ctrl + X` para salir

---

## 3️⃣ Verificar Conexión

```bash
python reddit_poster.py
```

Deberías ver:
```
✅ Conectado como /u/TU_USUARIO
📊 Karma: XXXX (Post: XXX, Comment: XXX)
```

---

## 4️⃣ Subreddits Disponibles

El bot intentará publicar en estos subreddits (según tu karma):

| Subreddit | Karma Mínimo | Tipo |
|-----------|--------------|------|
| r/InteligenciaArtificial | 0 | Español 🇪🇸 |
| r/IA | 0 | Español 🇪🇸 |
| r/ChatGPT | 100 | General |
| r/technews | 200 | Noticias |
| r/singularity | 300 | IA Avanzada |
| r/artificial | 500 | General |
| r/technology | 500 | Tech |
| r/MachineLearning | 1000 | Técnico |

### Si tienes poco karma:
1. **Comenta** en posts existentes (ganas karma rápido)
2. **Publica contenido útil** sin promoción
3. **Espera** unos días y vuelve a intentar

---

## 5️⃣ Publicar Contenido

### Publicación manual:

```bash
python reddit_poster.py
```

### Publicación automática (programada):

```bash
# Añadir al scheduler existente
# El bot publicará 3 veces al día con 4 horas de delay
```

---

## 📊 Estrategia de Contenido para Reddit

### ✅ LO QUE FUNCIONA:

1. **Herramientas gratuitas** - Siempre populares
2. **Tutoriales paso a paso** - Alto engagement
3. **Comparativas** - "X vs Y"
4. **Listas** - "Top 5 herramientas para..."
5. **Noticias exclusivas** - Primicias de IA

### ❌ LO QUE DEBES EVITAR:

1. **Spam puro** - Solo enlaces sin contexto
2. **Clickbait** - Títulos engañosos
3. **Autopromoción excesiva** - Máximo 10% de tus posts
4. **Ignorar reglas** - Cada subreddit tiene las suyas

---

## 🎯 Títulos que Funcionan

### Ejemplos probados:

```
🤖 Herramienta IA del Día: [Nombre]
- Esta herramienta gratuita hace [X] en segundos

📰 Noticia IA: [Título impactante]
- Resumen de 2-3 líneas del anuncio

💡 Tip de IA: Cómo [lograr X] con IA
- Tutorial paso a paso

📦 Recurso Gratuito: [Nombre del curso/recurso]
- Normalmente cuesta $X, hoy gratis
```

---

## 🔧 Comandos Útiles

```bash
# Verificar estado
python reddit_poster.py

# Ver logs en vivo
tail -f logs/reddit_*.log

# Ver configuración
cat reddit_config.json

# Ver subreddits disponibles
python -c "
import json
with open('reddit_config.json') as f:
    config = json.load(f)
for sub in config['subreddits']:
    print(f\"r/{sub['name']} - {sub['min_karma']} karma\")
"
```

---

## ⚠️ Reglas Importantes

### Para evitar baneos:

1. **No publiques más de 3-5 veces al día** en total
2. **Espera al menos 1 hora** entre posts
3. **Varía los subreddits** - no publiques lo mismo en todos
4. **Participa genuinamente** - comenta, vota, sé parte de la comunidad
5. **Respeta las reglas** de cada subreddit

### Si te banean:
- Revisa las reglas del subreddit
- Espera 24-48 horas
- Comienza con participación orgánica
- Vuelve a intentar con contenido de más valor

---

## 📈 Métricas a Seguir

| Métrica | Objetivo |
|---------|----------|
| Upvote ratio | >80% |
| Comments por post | 5+ |
| Clicks al canal | 50+/día |
| Nuevos suscriptores | 20+/día desde Reddit |

---

## 🚀 Tips de Crecimiento Rápido

### Semana 1:
- [ ] Configurar API
- [ ] Publicar 1-2 veces al día
- [ ] Comentar en posts populares

### Semana 2:
- [ ] Analizar qué posts funcionan mejor
- [ ] Duplicar el formato exitoso
- [ ] Aumentar a 3 posts/día

### Semana 3:
- [ ] Crear contenido "evergreen"
- [ ] Responder TODOS los comentarios
- [ ] Cross-postear entre subreddits relacionados

---

## 🆘 Solución de Problemas

### Error: "Invalid client"
- Verifica que el **app type** sea **script**
- Revisa que copiaste bien el client_id (sin espacios)

### Error: "Unauthorized"
- Verifica username y password
- Asegúrate de que la cuenta no tenga 2FA sin configurar

### Error: "Too Many Requests"
- Reddit limita a 60 requests/minuto
- El bot ya incluye delays, espera unos minutos

### Error: "Subreddit banned"
- Fuiste baneado de ese subreddit
- Elimínalo de la lista o crea otra cuenta

---

## 📞 Recursos

- **Documentación PRAW:** https://praw.readthedocs.io/
- **Reddit API Rules:** https://www.reddit.com/wiki/api
- **r/redditdev:** Para ayuda técnica

---

**¡Listo! Ahora tu contenido de IA llegará a miles de personas en Reddit** 🚀
