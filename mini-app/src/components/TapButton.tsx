import { useState } from 'react'
import { motion } from 'framer-motion'

interface TapButtonProps {
  onTap: () => void
}

export default function TapButton({ onTap }: TapButtonProps) {
  const [clicks, setClicks] = useState<{ id: number; x: number; y: number }[]>([])

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    
    // Add click effect
    const newClick = { id: Date.now(), x, y }
    setClicks(prev => [...prev, newClick])
    
    // Remove click effect after animation
    setTimeout(() => {
      setClicks(prev => prev.filter(c => c.id !== newClick.id))
    }, 1000)
    
    // Call game tap
    onTap()
  }

  return (
    <div className="relative flex justify-center">
      <motion.button
        onClick={handleClick}
        className="w-64 h-64 rounded-full bg-gradient-to-br from-yellow-400 via-yellow-500 to-yellow-600 
                   shadow-2xl flex items-center justify-center relative overflow-hidden
                   active:scale-95 transition-transform duration-100
                   border-8 border-yellow-300"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {/* Shine effect */}
        <div className="absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b from-white to-transparent opacity-30"></div>
        
        {/* Robot emoji */}
        <span className="text-8xl relative z-10">🤖</span>
        
        {/* Click effects */}
        {clicks.map((click) => (
          <motion.div
            key={click.id}
            className="absolute text-2xl font-bold text-white pointer-events-none"
            style={{ left: click.x, top: click.y }}
            initial={{ opacity: 1, y: 0, scale: 1 }}
            animate={{ opacity: 0, y: -50, scale: 1.5 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
          >
            +1 💰
          </motion.div>
        ))}
        
        {/* Rotating border effect */}
        <div className="absolute inset-0 rounded-full border-4 border-dashed border-white border-opacity-30 animate-spin-slow"></div>
      </motion.button>
      
      {/* Glow effect */}
      <div className="absolute inset-0 bg-yellow-500 rounded-full blur-3xl opacity-20 animate-pulse"></div>
    </div>
  )
}
