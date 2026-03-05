# 🚀 Deploy Rápido en fly.io

## Pasos para deployar tu bot en 5 minutos

### 1️⃣ Instalar flyctl

Abre PowerShell (Windows) y ejecuta:

```powershell
winget install fly.flyctl
```

### 2️⃣ Iniciar sesión

```bash
fly auth login
```

Se abrirá tu navegador. Inicia sesión con GitHub.

### 3️⃣ Configurar nombre único

Abre `fly.toml` y cambia:

```toml
app = "iadaily-bot-unico"  # Pon un nombre único
```

### 4️⃣ Subir cambios a GitHub

```bash
git add .
git commit -m "🚀 Deploy a fly.io"
git push
```

### 5️⃣ Crear app en fly.io

```bash
fly launch --no-deploy --region mad --name iadaily-bot-unico
```

### 6️⃣ Configurar secrets

```bash
fly secrets set TELEGRAM_BOT_TOKEN="8627686733:AAGgyqXtPu1juP1hjGZbb0iIhJWhq2WN324"
fly Secrets set TELEGRAM_CHANNEL_ID="@IADailyChannel"
fly secrets set TELEGRAM_ADMIN_USERS="2036304183"
```

### 7️⃣ Deploy

```bash
fly deploy --remote-only
```

### 8️⃣ Verificar

```bash
fly status
fly logs
```

### 9️⃣ Probar el bot

1. Abre Telegram
2. Busca tu bot: `@IADaily_Bot`
3. Envía `/start`
4. ¡Debería responder!

---

## ✅ ¡Listo!

Tu bot ahora funciona 24/7 en la nube.

**Comandos útiles:**

```bash
fly status          # Ver estado
fly logs            # Ver logs
fly restart         # Reiniciar
fly ssh console     # Consola SSH
```

---

## 📊 Costo

**Free tier:** $0/mes (tu bot usa muy pocos recursos)

---

## ⚠️ Problemas comunes

### "App name already taken"
Cambia el nombre en `fly.toml` a algo único.

### "Not authenticated"
Ejecuta: `fly auth login`

### El bot no responde
Revisa logs: `fly logs` y verifica el token.
