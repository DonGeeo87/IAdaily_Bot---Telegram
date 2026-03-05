/// <reference types="vite/client" />

// Telegram WebApp types
interface TelegramWebApp {
  ready(): void
  expand(): void
  close(): void
  showConfirm(message: string): Promise<boolean>
  showPopup(params: any): void
  showAlert(message: string): void
  HapticFeedback: {
    impactOccurred(style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft'): void
    notificationOccurred(type: 'success' | 'warning' | 'error'): void
    selectionChanged(): void
  }
  MainButton: {
    text: string
    color: string
    textColor: string
    isVisible: boolean
    isActive: boolean
    show(): void
    hide(): void
    enable(): void
    disable(): void
    onClick(callback: () => void): void
    offClick(callback: () => void): void
  }
  BackButton: {
    isVisible: boolean
    show(): void
    hide(): void
    onClick(callback: () => void): void
    offClick(callback: () => void): void
  }
  themeParams: {
    bg_color: string
    text_color: string
    hint_color: string
    link_color: string
    button_color: string
    button_text_color: string
    secondary_bg_color: string
  }
  colorScheme: 'light' | 'dark'
  platform: 'android' | 'ios' | 'macos' | 'web' | 'tdesktop'
  version: string
  initData: string
  initDataUnsafe: {
    query_id?: string
    user?: {
      id: number
      first_name: string
      last_name?: string
      username?: string
      language_code: string
    }
  }
}

interface Window {
  Telegram: {
    WebApp: TelegramWebApp
  }
}
