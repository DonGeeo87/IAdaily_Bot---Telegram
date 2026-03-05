import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Confetti from 'react-confetti'
import { useGameStore } from './store/gameStore'
import { formatNumber, formatCoins } from './utils/formatters'
import Header from './components/Header'
import BottomNav from './components/BottomNav'
import TapButton from './components/TapButton'
import EnergyBar from './components/EnergyBar'

function App() {
  const { 
    coins, 
    gems, 
    level, 
    xp, 
    xpToNextLevel,
    energy,
    maxEnergy,
    coinsPerTap,
    coinsPerSecond,
    tap,
    buyUpgrade,
    buyEnergy
  } = useGameStore()

  const [showConfetti, setShowConfetti] = useState(false)
  const [activeTab, setActiveTab] = useState<'home' | 'upgrades' | 'missions' | 'profile'>('home')

  // Check for level up
  useEffect(() => {
    if (xp >= xpToNextLevel) {
      setShowConfetti(true)
      setTimeout(() => setShowConfetti(false), 5000)
    }
  }, [xp, xpToNextLevel])

  // Auto-save every 30 seconds
  useEffect(() => {
    const saveInterval = setInterval(() => {
      useGameStore.persist.persist()
    }, 30000)

    return () => clearInterval(saveInterval)
  }, [])

  return (
    <div className="min-h-screen bg-telegram-bg text-telegram-text pb-20">
      {showConfetti && <Confetti />}
      
      {/* Header */}
      <Header />

      {/* Main Content */}
      <main className="px-4 py-4 space-y-4">
        {activeTab === 'home' && (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-2 gap-3">
              <motion.div 
                className="card gradient-gold"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.1 }}
              >
                <div className="text-2xl mb-1">💰</div>
                <div className="text-xs opacity-80">Coins</div>
                <div className="text-lg font-bold">{formatNumber(coins)}</div>
              </motion.div>

              <motion.div 
                className="card gradient-purple"
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <div className="text-2xl mb-1">💎</div>
                <div className="text-xs opacity-80">Gems</div>
                <div className="text-lg font-bold">{formatNumber(gems)}</div>
              </motion.div>
            </div>

            {/* Income Stats */}
            <motion.div 
              className="card"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <div className="flex justify-between items-center">
                <div>
                  <div className="text-sm text-telegram-hint">Income</div>
                  <div className="text-xl font-bold text-success">
                    +{formatNumber(coinsPerSecond)} coins/sec
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-telegram-hint">Per Tap</div>
                  <div className="text-xl font-bold text-accent">
                    +{formatNumber(coinsPerTap)}
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Energy Bar */}
            <EnergyBar current={energy} max={maxEnergy} />

            {/* Tap Button */}
            <div className="py-8">
              <TapButton onTap={tap} />
            </div>

            {/* Quick Upgrades */}
            <motion.div 
              className="card"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              <h3 className="text-lg font-bold mb-3">⚡ Mejoras Rápidas</h3>
              <div className="space-y-2">
                <button
                  onClick={() => buyUpgrade('gpu')}
                  className="w-full btn-secondary flex justify-between items-center"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🖥️</span>
                    <span>GPU Upgrade</span>
                  </div>
                  <div className="text-right">
                    <div className="text-accent font-bold">
                      {formatCoins(useGameStore.getState().upgrades.gpu.cost)}
                    </div>
                    <div className="text-xs text-telegram-hint">
                      +{formatCoins(useGameStore.getState().upgrades.gpu.bonus)} CPS
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => buyUpgrade('model')}
                  className="w-full btn-secondary flex justify-between items-center"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-xl">🧠</span>
                    <span>AI Model</span>
                  </div>
                  <div className="text-right">
                    <div className="text-accent font-bold">
                      {formatCoins(useGameStore.getState().upgrades.model.cost)}
                    </div>
                    <div className="text-xs text-telegram-hint">
                      +{formatCoins(useGameStore.getState().upgrades.model.bonus)} CPS
                    </div>
                  </div>
                </button>
              </div>
            </motion.div>

            {/* Daily Bonus */}
            <motion.div 
              className="card gradient-blue"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-bold text-lg">🎁 Bonus Diario</h3>
                  <p className="text-sm opacity-80">¡Reclama tus coins gratis!</p>
                </div>
                <button className="btn-gold px-6">
                  Reclamar
                </button>
              </div>
            </motion.div>
          </>
        )}

        {activeTab === 'upgrades' && (
          <div className="space-y-3">
            <h2 className="text-2xl font-bold mb-4">🏪 Tienda de Mejoras</h2>
            
            {/* Data Centers */}
            <div className="card">
              <h3 className="font-bold mb-3">🏢 Data Centers</h3>
              <div className="space-y-2">
                {['Basic Server', 'GPU Cluster', 'Quantum Computer'].map((item, idx) => (
                  <button
                    key={item}
                    onClick={() => buyUpgrade(`datacenter_${idx}`)}
                    className="w-full btn-secondary flex justify-between items-center"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xl">🏢</span>
                      <div className="text-left">
                        <div className="font-bold">{item}</div>
                        <div className="text-xs text-telegram-hint">
                          Nivel {useGameStore.getState().upgrades[`datacenter_${idx}`]?.level || 0}
                        </div>
                      </div>
                    </div>
                    <div className="text-accent font-bold">
                      {formatCoins(useGameStore.getState().upgrades[`datacenter_${idx}`]?.cost || 100 * Math.pow(2, idx))}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* AI Models */}
            <div className="card">
              <h3 className="font-bold mb-3">🤖 Modelos de IA</h3>
              <div className="space-y-2">
                {['GPT-3', 'GPT-4', 'Claude', 'Gemini', 'Qwen'].map((model, idx) => (
                  <button
                    key={model}
                    onClick={() => buyUpgrade(`model_${idx}`)}
                    className="w-full btn-secondary flex justify-between items-center"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xl">🧠</span>
                      <div className="text-left">
                        <div className="font-bold">{model}</div>
                        <div className="text-xs text-telegram-hint">
                          Nivel {useGameStore.getState().upgrades[`model_${idx}`]?.level || 0}
                        </div>
                      </div>
                    </div>
                    <div className="text-accent font-bold">
                      {formatCoins(useGameStore.getState().upgrades[`model_${idx}`]?.cost || 500 * Math.pow(3, idx))}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'missions' && (
          <div className="space-y-3">
            <h2 className="text-2xl font-bold mb-4">🎯 Misiones Diarias</h2>
            
            <div className="card">
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">👆</span>
                  <div>
                    <div className="font-bold">Tap Master</div>
                    <div className="text-xs text-telegram-hint">0 / 1000 taps</div>
                  </div>
                </div>
                <div className="text-accent font-bold">+500 💰</div>
              </div>
              <div className="w-full bg-telegram-secondary rounded-full h-2">
                <div className="bg-primary h-2 rounded-full" style={{ width: '0%' }}></div>
              </div>
            </div>

            <div className="card">
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">🧠</span>
                  <div>
                    <div className="font-bold">Trivia Challenge</div>
                    <div className="text-xs text-telegram-hint">0 / 5 correctas</div>
                  </div>
                </div>
                <div className="text-accent font-bold">+1000 💰</div>
              </div>
              <div className="w-full bg-telegram-secondary rounded-full h-2">
                <div className="bg-success h-2 rounded-full" style={{ width: '0%' }}></div>
              </div>
            </div>

            <div className="card gradient-purple">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-bold">🎲 Trivia IA</h3>
                  <p className="text-sm opacity-80">¡Responde y gana coins!</p>
                </div>
                <button className="btn-gold px-6">
                  Jugar
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="space-y-4">
            <div className="card text-center py-8">
              <div className="text-6xl mb-4">👤</div>
              <h2 className="text-2xl font-bold">
                {window.Telegram.WebApp.initDataUnsafe?.user?.first_name || 'Jugador'}
              </h2>
              <p className="text-telegram-hint">Nivel {level}</p>
              
              <div className="mt-4">
                <div className="text-sm text-telegram-hint mb-1">XP Progress</div>
                <div className="w-full bg-telegram-secondary rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-yellow-400 to-yellow-600 h-3 rounded-full transition-all"
                    style={{ width: `${(xp / xpToNextLevel) * 100}%` }}
                  ></div>
                </div>
                <div className="text-xs text-telegram-hint mt-1">
                  {xp} / {xpToNextLevel} XP
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="card text-center">
                <div className="text-2xl mb-2">🏆</div>
                <div className="text-2xl font-bold">0</div>
                <div className="text-xs text-telegram-hint">Ranking</div>
              </div>
              <div className="card text-center">
                <div className="text-2xl mb-2">🔥</div>
                <div className="text-2xl font-bold">0</div>
                <div className="text-xs text-telegram-hint">Racha</div>
              </div>
              <div className="card text-center">
                <div className="text-2xl mb-2">🎮</div>
                <div className="text-2xl font-bold">0</div>
                <div className="text-xs text-telegram-hint">Partidas</div>
              </div>
              <div className="card text-center">
                <div className="text-2xl mb-2">⭐</div>
                <div className="text-2xl font-bold">0</div>
                <div className="text-xs text-telegram-hint">Logros</div>
              </div>
            </div>

            <div className="card">
              <h3 className="font-bold mb-3">⚙️ Configuración</h3>
              <div className="space-y-2">
                <button className="w-full btn-secondary text-left">
                  🔊 Sonido: ON
                </button>
                <button className="w-full btn-secondary text-left">
                  📱 Vibración: ON
                </button>
                <button className="w-full btn-secondary text-left">
                  🌐 Idioma: Español
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Bottom Navigation */}
      <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />
    </div>
  )
}

export default App
