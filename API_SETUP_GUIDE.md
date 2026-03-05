# 🔌 Configuración de APIs Gratuitas

## 📋 APIs Disponibles

El bot soporta las siguientes APIs gratuitas para contenido automático:

---

## 1️⃣ GNews API - Noticias en Tiempo Real

**Función:** Obtener noticias de IA automáticamente

### Obtener API Key (2 minutos):

1. **Ve a:** https://gnews.io/
2. **Click en:** "Get Your Free API Key"
3. **Regístrate** con Google o email
4. **Copia tu API key** (aparece inmediatamente)

### Configurar en el bot:

```bash
# Método 1: Desde Telegram
/setgnews TU_API_KEY_AQUI

# Método 2: Editar archivo
nano apis_config.json
```

### Límites:
- ✅ **100 requests/día** gratis
- ✅ No requiere tarjeta de crédito
- ✅ Válido por 30 días (renovable)

---

## 2️⃣ Hugging Face API - IA Avanzada

**Función:** Generar contenido con modelos de IA

### Obtener API Token (3 minutos):

1. **Ve a:** https://huggingface.co/
2. **Crea cuenta** gratis
3. **Ve a:** Settings → Access Tokens
4. **Click:** "New token" → Role: "read"
5. **Copia tu token**

### Configurar en el bot:

```bash
/sethf TU_TOKEN_AQUI
```

### Límites:
- ✅ **30,000 requests/mes** gratis
- ✅ Modelos: google/flan-t5-large, etc.
- ✅ No requiere tarjeta

---

## 3️⃣ Pexels API - Imágenes Gratis

**Función:** Obtener imágenes para posts

### Obtener API Key (2 minutos):

1. **Ve a:** https://www.pexels.com/api/
2. **Click:** "Sign Up"
3. **Regístrate** gratis
4. **Ve a:** Your Apps → Create App
5. **Copia tu API key**

### Configurar en el bot:

```bash
/setpexels TU_API_KEY_AQUI
```

### Límites:
- ✅ **Unlimited requests**
- ✅ 10,000 fotos/mes aprox
- ✅ No requiere tarjeta

---

## 4️⃣ APIs Sin Configuración (Ya incluidas)

### Quotable API - Frases
- ✅ Sin API key
- ✅ Frases inspiradoras aleatorias
- ✅ Unlimited

### Wikipedia API
- ✅ Sin API key
- ✅ Artículos aleatorios
- ✅ Unlimited

---

## 🚀 Comandos de Configuración

### Ver estado de APIs:
```
/setup
```

### Configurar cada API:
```
/setgnews [API_KEY]
/sethf [TOKEN]
/setpexels [API_KEY]
```

### Verificar configuración:
```bash
cat apis_config.json
```

---

## 📊 Comparación de APIs

| API | Gratis | Rate Limit | Requiere CC | Dificultad |
|-----|--------|------------|-------------|------------|
| GNews | ✅ | 100/día | ❌ | Fácil |
| Hugging Face | ✅ | 30k/mes | ❌ | Media |
| Pexels | ✅ | Unlimited | ❌ | Fácil |
| Quotable | ✅ | Unlimited | ❌ | Muy Fácil |
| Wikipedia | ✅ | Unlimited | ❌ | Muy Fácil |

---

## 💡 Recomendación de Configuración

### Mínimo (5 minutos):
- [x] Quotable (ya incluido)
- [x] Wikipedia (ya incluido)

### Estándar (10 minutos):
- [x] GNews API
- [x] Pexels API

### Completo (15 minutos):
- [x] GNews API
- [x] Hugging Face
- [x] Pexels API

---

## 🔍 Verificar que Funciona

### Probar noticias:
```
/noticias
```

### Probar generación:
```
/generar
```

### Ver logs:
```bash
tail -f logs/bot_*.log
```

---

## ⚠️ Solución de Problemas

### Error: "Invalid API Key"
- Verifica que copiaste bien la key (sin espacios)
- Revisa que la API esté activa en tu cuenta

### Error: "Rate limit exceeded"
- Espera al día siguiente (se resetea a 00:00 UTC)
- Considera usar otra API como fallback

### Error: "API no responde"
- Verifica tu conexión a internet
- Revisa el status de la API en su website

---

## 🎯 Ejemplo de apis_config.json

```json
{
  "gnews": {
    "api_key": "abc123xyz456",
    "enabled": true,
    "endpoint": "https://gnews.io/api/v4/top-headlines",
    "rate_limit": "100 req/día"
  },
  "huggingface": {
    "api_key": "hf_abc123xyz",
    "enabled": true,
    "endpoint": "https://api-inference.huggingface.co/models",
    "model": "google/flan-t5-large",
    "rate_limit": "30k req/mes"
  },
  "pexels": {
    "api_key": "pexels_abc123",
    "enabled": true,
    "endpoint": "https://api.pexels.com/v1/search",
    "rate_limit": "Unlimited"
  },
  "quotable": {
    "enabled": true,
    "endpoint": "http://api.quotable.io/random"
  },
  "wikipedia": {
    "enabled": true,
    "endpoint": "https://es.wikipedia.org/api/rest_v1/page/random/summary"
  }
}
```

---

## 📈 Próximas APIs a Agregar

- [ ] OpenWeather API (clima para posts)
- [ ] NASA API (imágenes del espacio)
- [ ] NewsAPI.org (más fuentes de noticias)
- [ ] Unsplash API (más imágenes)

¿Quieres que agregue alguna API específica? ¡Avísame!

---

**¡Configura al menos 1 API para contenido en tiempo real!** 🚀
