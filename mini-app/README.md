# 🤖 IA Clicker Empire - Telegram Mini App

Juego incremental tipo "Hamster Kombat" pero temático de Inteligencia Artificial.

## 🚀 Características

- 🏗️ **Construye tu imperio IA**: Compra GPUs, modelos, data centers
- 💰 **Sistema económico**: Coins y Gems
- ⚡ **Energía**: Sistema de energía que se regenera
- 🎯 **Misiones diarias**: Trivia y desafíos
- 🏆 **Leaderboard**: Compite con otros jugadores
- 🎁 **Bonus diario**: Recompensas por jugar cada día
- 📊 **Progresión**: Sube de nivel y desbloquea contenido

## 📁 Estructura

```
mini-app/
├── frontend/           # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/ # Componentes React
│   │   ├── store/      # Zustand store
│   │   ├── utils/      # Utilidades
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── backend/            # FastAPI Python
│   ├── main.py
│   └── requirements.txt
└── README.md
```

## 🛠️ Instalación

### Frontend

```bash
cd mini-app
npm install
npm run dev
```

### Backend

```bash
cd mini-app/backend
pip install -r requirements.txt
python main.py
```

## 🚀 Deploy

### Frontend (Vercel)

```bash
npm run build
vercel deploy --prod
```

### Backend (Fly.io)

```bash
fly launch
fly deploy
```

## 🎮 Cómo Jugar

1. **Toca el robot** 🤖 para ganar coins
2. **Compra mejoras** para aumentar income pasivo
3. **Completa misiones** para bonus extra
4. **Responde trivia** para ganar coins y XP
5. **Sube de nivel** para desbloquear contenido

## 💰 Mejoras Disponibles

| Mejora | Costo Base | Bonus CPS |
|--------|------------|-----------|
| GPU Upgrade | 50 | +1 |
| AI Model | 100 | +2 |
| Data Center | 500 | +10 |
| Dataset | 200 | +3 |
| Team | 1000 | +25 |

## 🎯 Trivia

- 5 preguntas diarias
- Dificultad variable
- Recompensas: 100-500 coins
- Bonus: +XP por respuesta correcta

## 🔧 Configuración en Telegram Bot

1. Crea un nuevo bot con @BotFather
2. Usa `/newapp` para crear Mini App
3. Configura la URL del frontend
4. ¡Listo!

## 📊 Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Zustand (state management)
- Framer Motion (animaciones)
- Telegram WebApp SDK

### Backend
- FastAPI
- SQLite
- Uvicorn

## 🎨 Assets

Los assets gráficos (emojis) son estándar de Unicode.
Para producción, considerar:
- Iconos personalizados
- Animaciones Lottie
- Sprites para efectos

## 📈 Próximas Features

- [ ] Batallas PvP
- [ ] Guilds/Clanes
- [ ] Eventos semanales
- [ ] Sistema de referidos
- [ ] Tienda de skins
- [ ] Logros raros
- [ ] Temporadas ranking

## 🐛 Bugs Conocidos

- Ninguno reportado (versión alpha)

## 📝 Licencia

MIT

---

**¡Diviértete construyendo tu imperio IA! 🚀**
