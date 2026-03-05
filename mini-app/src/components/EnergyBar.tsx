interface EnergyBarProps {
  current: number
  max: number
}

export default function EnergyBar({ current, max }: EnergyBarProps) {
  const percentage = (current / max) * 100
  
  let colorClass = 'bg-success'
  if (percentage < 25) colorClass = 'bg-danger'
  else if (percentage < 50) colorClass = 'bg-accent'
  
  return (
    <div className="card">
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xl">⚡</span>
          <span className="font-bold">Energía</span>
        </div>
        <span className="text-sm font-bold">
          {current} / {max}
        </span>
      </div>
      
      <div className="w-full bg-telegram-bg rounded-full h-4 overflow-hidden">
        <div 
          className={`h-full ${colorClass} transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        >
          {/* Animated shine */}
          <div className="w-full h-full bg-gradient-to-r from-transparent via-white to-transparent opacity-20 animate-pulse"></div>
        </div>
      </div>
      
      <div className="text-xs text-telegram-hint mt-1">
        Regeneración: 1 ⚡ / segundo
      </div>
    </div>
  )
}
