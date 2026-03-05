import { useGameStore } from '../store/gameStore'
import { formatNumber } from '../utils/formatters'

export default function Header() {
  const { level, xp, xpToNextLevel } = useGameStore()
  
  return (
    <header className="bg-telegram-secondary p-4 rounded-b-2xl shadow-lg">
      <div className="flex justify-between items-center mb-3">
        <div>
          <h1 className="text-2xl font-bold">🤖 IA Clicker</h1>
          <p className="text-sm text-telegram-hint">Construye tu imperio IA</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-telegram-hint">Nivel {level}</div>
          <div className="text-xs text-accent">
            {xp}/{xpToNextLevel} XP
          </div>
        </div>
      </div>
      
      {/* XP Progress Bar */}
      <div className="w-full bg-telegram-bg rounded-full h-2">
        <div 
          className="bg-gradient-to-r from-yellow-400 to-yellow-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${(xp / xpToNextLevel) * 100}%` }}
        ></div>
      </div>
    </header>
  )
}
