import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Inicializar Telegram WebApp
const tg = window.Telegram.WebApp
tg.ready()
tg.expand()

// Configurar colores del tema
document.documentElement.style.setProperty('--tg-theme-bg-color', tg.backgroundColor || '#1c242f')
document.documentElement.style.setProperty('--tg-theme-text-color', tg.textColor || '#ffffff')

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
