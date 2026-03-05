# 🤖 IA Daily Bot - Guía Completa Actualizada

## ✅ Cambios Recientes

### 1. **Recomendación de IAs (PÚBLICO)**
- `/recomendar` - Recibe una plataforma de IA al azar
- 15 IAs diferentes: ChatGPT, Claude, Gemini, Qwen, DeepSeek, MiniMax, Ollama, etc.

### 2. **Prompts Multi-IA (PÚBLICO)**
- `/prompts` - Prompts para TODAS las IAs famosas
- Incluye: ChatGPT, Claude, Gemini, Qwen, DeepSeek, MiniMax, Ollama, Midjourney, Suno, Runway, ElevenLabs

### 3. **Panel de Modelos Qwen/Wan (SOLO OWNER)**
- `/modelos` - Ver todos los modelos con cuotas
- `/usarmodelo [nombre] [prompt]` - Usar modelo específico

---

## 📊 Comandos Disponibles

### 🟢 PÚBLICOS (Todos los usuarios):

| Comando | Función |
|---------|---------|
| `/start` | Iniciar bot con menú |
| `/recomendar` | **NUEVO** - IA aleatoria recomendada |
| `/noticias` | Noticias de IA |
| `/prompts` | **ACTUALIZADO** - Prompts para todas las IAs |
| `/stats` | Estadísticas del canal |
| `/help` | Ayuda completa |

### 🔴 SOLO OWNER (Tú):

| Comando | Función |
|---------|---------|
| `/qwen [pregunta]` | Chat con IA real |
| `/qwennews [tema]` | Generar noticia |
| `/qwentool [nombre]` | Review herramienta |
| `/qwenprompt [cat]` | Generar prompt |
| `/modelos` | **NUEVO** - Ver modelos Qwen/Wan |
| `/usarmodelo [nombre] [prompt]` | **NUEVO** - Usar modelo específico |
| `/security` | Ver seguridad |
| `/grant [user] [rol]` | Dar permisos |
| `/ban [user]` | Banear usuario |

---

## 🎯 IAs Disponibles para Recomendación

1. **ChatGPT** - El más popular. Texto y código.
2. **Claude** - Análisis y escritura larga.
3. **Gemini** - Google. Multimodal.
4. **Qwen** - Alibaba. Excelente en español.
5. **DeepSeek** - Código y matemáticas.
6. **MiniMax** - Razonamiento avanzado.
7. **Ollama** - Modelos locales. Privacidad.
8. **Perplexity** - Búsqueda con fuentes.
9. **Midjourney** - Imágenes artísticas.
10. **Runway** - Video y edición.
11. **ElevenLabs** - Voces sintéticas.
12. **Suno** - Música con IA.
13. **Gamma** - Presentaciones.
14. **Notion AI** - Notas con IA.
15. **Cursor** - Editor de código.

---

## 📝 Modelos Qwen/Wan Disponibles

### Texto:
- `qwen3.5-397b-a17b` - 1M tokens (vence: 17/05/2026)
- `qwen3.5-122b-a10b` - 1M tokens (vence: 24/05/2026)
- `qwen3.5-35b-a3b` - 1M tokens (vence: 24/05/2026)
- `qwen3.5-27b` - 1M tokens (vence: 24/05/2026)
- `qwen3.5-plus` - 1M tokens (vence: 17/05/2026)
- `qwen3.5-flash` - 1M tokens (vence: 24/05/2026)
- `qwen3-max` - 1M tokens (vence: 26/04/2026)

### Código:
- `qwen3-coder-next` - 1M tokens (vence: 05/05/2026)

### Visión:
- `qwen3-vl-plus` - 1M tokens (vence: 19/03/2026)
- `qwen3-vl-flash` - 1M tokens (vence: 26/04/2026)

### Roleplay:
- `qwen-plus-character` - 1M tokens (vence: 28/04/2026)
- `qwen-flash-character` - 1M tokens (vence: N/A)

### Video:
- `wan2.2-kf2v-flash` - 50 usos (vence: 06/04/2026)

---

## 🚀 Ejemplos de Uso

### Público:

```
# Obtener recomendación de IA
/recomendar

# Obtener prompt para IA aleatoria
/prompts
```

### Owner (Tú):

```
# Ver modelos disponibles
/modelos

# Usar modelo específico
/usarmodelo qwen3.5-397b-a17b ¿Qué es el machine learning?

# Chat normal con Qwen
/qwen Explica la computación cuántica

# Generar noticia
/qwennews Avances en IA 2026

# Review de herramienta
/qwentool Notion AI

# Generar prompt
/qwenprompt marketing digital
```

---

## 📁 Archivos del Sistema

| Archivo | Función |
|---------|---------|
| `bot_robusto.py` | Bot principal |
| `security_manager.py` | Sistema de permisos |
| `security.json` | Usuarios y roles |
| `qwen_ai.py` | Integración Qwen |
| `qwen_config.json` | API key de Qwen |
| `modelos_config.json` | **NUEVO** - Modelos y cuotas |
| `apis_config.json` | Otras APIs (GNews, Pexels, etc.) |

---

## 🔐 Seguridad

- `/recomendar` y `/prompts` son **públicos** (nivel 10)
- `/generar` (contenido local) sigue siendo **público**
- `/modelos` y `/usarmodelo` son **SOLO OWNER** (nivel 100)
- Comandos Qwen son **SOLO OWNER**

---

## 💡 Tips de Uso

### Para el Canal:
1. Usa `/recomendar` para obtener IA del día
2. Copia la recomendación
3. Publica en el canal

### Para Contenido Premium:
1. Usa `/qwennews [tema]` para noticia profesional
2. Usa `/qwentool [herramienta]` para review detallada
3. Usa `/usarmodelo qwen3-max [prompt]` para máxima calidad

### Para Ahorrar Tokens:
- Usa `qwen3.5-flash` para tareas simples
- Usa `qwen3.5-397b-a17b` para tareas complejas
- Usa `wan2.2-kf2v-flash` solo para video (50 usos limitados)

---

## 📊 Estadísticas de Cuotas

| Tipo | Total Tokens | Usados | Disponibles |
|------|--------------|--------|-------------|
| Texto | 8M | 0 | 8M |
| Código | 1M | 0 | 1M |
| Visión | 2M | 0 | 2M |
| Roleplay | 2M | 0 | 2M |
| Video | 50 usos | 0 | 50 |

---

**¡Tu bot ahora tiene IA real multi-plataforma!** 🚀
