import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface Upgrade {
  level: number
  cost: number
  bonus: number
}

interface GameState {
  // Currency
  coins: number
  gems: number
  
  // Progress
  level: number
  xp: number
  xpToNextLevel: number
  
  // Energy
  energy: number
  maxEnergy: number
  energyRegenRate: number
  
  // Stats
  coinsPerTap: number
  coinsPerSecond: number
  totalTaps: number
  totalCoinsEarned: number
  
  // Upgrades
  upgrades: {
    gpu: Upgrade
    model: Upgrade
    datacenter: Upgrade
    dataset: Upgrade
    team: Upgrade
  }
  
  // Achievements
  achievements: string[]
  
  // Actions
  tap: () => void
  buyUpgrade: (type: string) => void
  buyEnergy: () => void
  addCoins: (amount: number) => void
  addGems: (amount: number) => void
  addXp: (amount: number) => void
  claimDailyBonus: () => void
}

const calculateUpgradeCost = (baseCost: number, level: number): number => {
  return Math.floor(baseCost * Math.pow(1.5, level))
}

export const useGameStore = create<GameState>()(
  persist(
    (set, get) => ({
      // Initial state
      coins: 100,
      gems: 10,
      level: 1,
      xp: 0,
      xpToNextLevel: 100,
      energy: 100,
      maxEnergy: 100,
      energyRegenRate: 1,
      coinsPerTap: 1,
      coinsPerSecond: 0,
      totalTaps: 0,
      totalCoinsEarned: 100,
      
      upgrades: {
        gpu: { level: 0, cost: 50, bonus: 1 },
        model: { level: 0, cost: 100, bonus: 2 },
        datacenter: { level: 0, cost: 500, bonus: 10 },
        dataset: { level: 0, cost: 200, bonus: 3 },
        team: { level: 0, cost: 1000, bonus: 25 },
      },
      
      achievements: [],
      
      // Tap action
      tap: () => {
        const state = get()
        if (state.energy < 1) return
        
        const coinsEarned = state.coinsPerTap
        const xpGained = 1
        
        set({
          coins: state.coins + coinsEarned,
          xp: state.xp + xpGained,
          energy: state.energy - 1,
          totalTaps: state.totalTaps + 1,
          totalCoinsEarned: state.totalCoinsEarned + coinsEarned,
        })
        
        // Haptic feedback
        if (window.Telegram?.WebApp?.HapticFeedback) {
          window.Telegram.WebApp.HapticFeedback.impactOccurred('light')
        }
        
        // Level up check
        const newXp = state.xp + xpGained
        if (newXp >= state.xpToNextLevel) {
          set({
            level: state.level + 1,
            xp: newXp - state.xpToNextLevel,
            xpToNextLevel: Math.floor(state.xpToNextLevel * 1.5),
            maxEnergy: state.maxEnergy + 10,
            energy: state.maxEnergy,
          })
          
          // Notification
          if (window.Telegram?.WebApp?.HapticFeedback) {
            window.Telegram.WebApp.HapticFeedback.notificationOccurred('success')
          }
        }
      },
      
      // Buy upgrade
      buyUpgrade: (type: string) => {
        const state = get()
        const upgrade = state.upgrades[type as keyof typeof state.upgrades]
        
        if (!upgrade || state.coins < upgrade.cost) return
        
        const newCoinsPerSecond = state.coinsPerSecond + upgrade.bonus
        
        set({
          coins: state.coins - upgrade.cost,
          upgrades: {
            ...state.upgrades,
            [type]: {
              ...upgrade,
              level: upgrade.level + 1,
              cost: calculateUpgradeCost(upgrade.cost, upgrade.level + 1),
            },
          },
          coinsPerSecond: newCoinsPerSecond,
        })
        
        // Haptic feedback
        if (window.Telegram?.WebApp?.HapticFeedback) {
          window.Telegram.WebApp.HapticFeedback.impactOccurred('medium')
        }
      },
      
      // Buy energy
      buyEnergy: () => {
        const state = get()
        const cost = 50 // gems
        
        if (state.gems < cost || state.energy >= state.maxEnergy) return
        
        set({
          gems: state.gems - cost,
          energy: state.maxEnergy,
        })
      },
      
      // Add coins
      addCoins: (amount: number) => {
        set({
          coins: get().coins + amount,
          totalCoinsEarned: get().totalCoinsEarned + amount,
        })
      },
      
      // Add gems
      addGems: (amount: number) => {
        set({ gems: get().gems + amount })
      },
      
      // Add XP
      addXp: (amount: number) => {
        const state = get()
        const newXp = state.xp + amount
        
        if (newXp >= state.xpToNextLevel) {
          set({
            level: state.level + 1,
            xp: newXp - state.xpToNextLevel,
            xpToNextLevel: Math.floor(state.xpToNextLevel * 1.5),
          })
        } else {
          set({ xp: newXp })
        }
      },
      
      // Claim daily bonus
      claimDailyBonus: () => {
        const state = get()
        const bonus = state.level * 100
        
        set({
          coins: state.coins + bonus,
          gems: state.gems + Math.floor(state.level / 5),
        })
      },
    }),
    
    {
      name: 'ia-clicker-save',
      partialize: (state) => ({
        coins: state.coins,
        gems: state.gems,
        level: state.level,
        xp: state.xp,
        energy: state.energy,
        upgrades: state.upgrades,
        achievements: state.achievements,
        coinsPerSecond: state.coinsPerSecond,
        totalTaps: state.totalTaps,
      }),
    }
  )
)

// Auto-regenerate energy and passive income
setInterval(() => {
  const state = useGameStore.getState()
  
  // Energy regen
  if (state.energy < state.maxEnergy) {
    useGameStore.setState({
      energy: Math.min(state.energy + state.energyRegenRate, state.maxEnergy)
    })
  }
  
  // Passive income
  if (state.coinsPerSecond > 0) {
    useGameStore.setState({
      coins: state.coins + state.coinsPerSecond,
      totalCoinsEarned: state.totalCoinsEarned + state.coinsPerSecond
    })
  }
}, 1000)
