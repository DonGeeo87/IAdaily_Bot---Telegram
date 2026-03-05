interface BottomNavProps {
  activeTab: 'home' | 'upgrades' | 'missions' | 'profile'
  setActiveTab: (tab: 'home' | 'upgrades' | 'missions' | 'profile') => void
}

export default function BottomNav({ activeTab, setActiveTab }: BottomNavProps) {
  const tabs = [
    { id: 'home', icon: '🏠', label: 'Inicio' },
    { id: 'upgrades', icon: '🏪', label: 'Tienda' },
    { id: 'missions', icon: '🎯', label: 'Misiones' },
    { id: 'profile', icon: '👤', label: 'Perfil' },
  ] as const

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-telegram-secondary border-t border-white border-opacity-10 px-4 py-2 safe-area-bottom">
      <div className="flex justify-around items-center max-w-md mx-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex flex-col items-center p-2 rounded-xl transition-all duration-200 ${
              activeTab === tab.id
                ? 'bg-primary text-white'
                : 'text-telegram-hint hover:bg-white hover:bg-opacity-5'
            }`}
          >
            <span className="text-2xl mb-1">{tab.icon}</span>
            <span className="text-xs font-medium">{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  )
}
