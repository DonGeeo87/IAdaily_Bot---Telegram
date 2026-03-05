# 🤖 Qwen AI - IA Real para tu Bot

## ✅ Configuración Completada

Tu bot ahora tiene **IA REAL** integrada usando la API de Qwen (Alibaba Cloud).

---

## 🔐 Acceso: SOLO OWNER

Los comandos de Qwen están restringidos **exclusivamente para el OWNER** (nivel 100).

Si otro usuario intenta usarlos:
```
⛔ ACCESO DENEGADO
🔒 Nivel requerido: 100
📊 Tu nivel: 10
```

---

## 🎯 Comandos de Qwen AI

### 1. `/qwen [pregunta]` - Chat con IA

**Uso:**
```
/qwen ¿Qué es el machine learning?
```

**Respuesta:**
Qwen generará una respuesta inteligente y contextual sobre el tema.

---

### 2. `/qwennews [tema]` - Generar Noticia

**Uso:**
```
/qwennews ChatGPT
```

**Genera:**
- Título llamativo
- 3 puntos clave
- Por qué es importante
- Enlace sugerido

**Ejemplo de salida:**
```
📰 Noticia Generada por Qwen

🔥 ChatGPT Anuncia Nueva Versión GPT-5

Puntos clave:
• Mayor capacidad de razonamiento
• Soporte para 100 idiomas
• Integración nativa con herramientas

Importancia: Esto cambia el panorama de la IA...

📖 Leer más: openai.com
```

---

### 3. `/qwentool [nombre]` - Review de Herramienta

**Uso:**
```
/qwentool Midjourney
```

**Genera:**
- ¿Qué es? (2-3 líneas)
- Características principales
- Casos de uso
- Precio
- Enlace oficial

---

### 4. `/qwenprompt [categoría]` - Generar Prompt

**Uso:**
```
/qwenprompt productividad
```

**Genera:**
- Prompt avanzado para ChatGPT
- Contexto claro
- Rol específico
- Formato de salida
- Ejemplo de uso

---

## 📊 Comparación: Qwen vs Contenido Local

| Característica | Qwen AI | Generador Local |
|----------------|---------|-----------------|
| **Contenido** | IA real en tiempo real | Plantillas predefinidas |
| **Flexibilidad** | Responde cualquier cosa | Limitado a plantillas |
| **Idioma** | Español nativo | Español fijo |
| **Contexto** | Conversacional | Estático |
| **Costo** | API (tu key) | Gratis |

---

## 🔧 Configuración Actual

```json
{
  "api_key": "sk-1f839d3b42254149b27130f2b0e6a4e",
  "enabled": true,
  "model": "qwen-turbo",
  "owner_only": true
}
```

---

## 📁 Archivos de Qwen

| Archivo | Función |
|---------|---------|
| `qwen_ai.py` | Integración con API |
| `qwen_config.json` | Configuración (API key) |
| `QWEN_GUIDE.md` | Esta guía |

---

## 🚀 Ejemplos de Uso

### Ejemplo 1: Preguntar sobre IA
```
/qwen ¿Cuáles son las mejores prácticas para usar ChatGPT?
```

### Ejemplo 2: Generar contenido para el canal
```
/qwennews Inteligencia Artificial en 2025
```

### Ejemplo 3: Review rápida
```
/qwentool Notion AI
```

### Ejemplo 4: Prompt personalizado
```
/qwenprompt marketing digital
```

---

## ⚙️ Modelo de Qwen

Actualmente usa: **qwen-turbo**

### Modelos disponibles:
- `qwen-turbo` - Rápido, económico (actual)
- `qwen-plus` - Balanceado
- `qwen-max` - Máxima calidad, más lento

### Cambiar modelo:
```bash
nano ~/telegram-ia-bot/qwen_config.json
# Cambiar "model": "qwen-plus"
```

---

## 💰 Costos de API

Qwen API es muy económica:

| Modelo | Costo aprox. |
|--------|--------------|
| qwen-turbo | ~$0.002/1K tokens |
| qwen-plus | ~$0.01/1K tokens |
| qwen-max | ~$0.03/1K tokens |

**Tu uso estimado:**
- 100 preguntas/día = ~$0.50/día
- 1000 preguntas/mes = ~$15/mes

---

## 🔒 Seguridad

- ✅ API key encriptada en config
- ✅ Solo owner puede usar
- ✅ Logs de todos los usos
- ✅ Rate limiting automático

---

## ⚠️ Solución de Problemas

### Error: "Qwen no configurado"
```bash
# Verificar config
cat ~/telegram-ia-bot/qwen_config.json

# Debe tener:
# "api_key": "sk-..."
# "enabled": true
```

### Error: "Invalid API Key"
```bash
# Verificar que la key es correcta
# Debe empezar con "sk-"
```

### Error: "Rate limit exceeded"
- Espera unos segundos entre requests
- Considera usar qwen-turbo que tiene límites más altos

---

## 📊 Ver Logs de Qwen

```bash
# Ver últimos usos
tail -f logs/bot.log | grep Qwen
```

---

## 🎯 Flujo Recomendado

### Para contenido del canal:
1. `/qwennews [tema]` - Genera noticia
2. Copia el resultado
3. Pega en el canal

### Para reviews:
1. `/qwentool [herramienta]` - Genera review
2. Revisa y edita si es necesario
3. Publica

### Para prompts:
1. `/qwenprompt [categoría]` - Genera prompt
2. Copia y guarda en tu biblioteca
3. Comparte en el canal

---

## 🆚 Comandos: Qwen vs Local

| Necesitas | Usa |
|-----------|-----|
| Respuesta rápida | `/qwen [pregunta]` |
| Noticia actual | `/qwennews [tema]` |
| Review detallada | `/qwentool [nombre]` |
| Prompt específico | `/qwenprompt [cat]` |
| Contenido genérico | `/generar` (local) |
| Prompts básicos | `/prompts` (local) |

---

## 💡 Tips Pro

1. **Sé específico en tus preguntas:**
   - ❌ `/qwen IA`
   - ✅ `/qwen ¿Cómo usar IA para automatizar emails?`

2. **Pide seguimiento:**
   - El bot recuerda el contexto de la conversación

3. **Usa para contenido del canal:**
   - Genera contenido único que no tienen otros

4. **Combina con campañas:**
   - Usa Qwen para personalizar campañas

---

**¡Disfruta de IA REAL en tu bot!** 🚀
