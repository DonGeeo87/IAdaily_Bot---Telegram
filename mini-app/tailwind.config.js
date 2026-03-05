/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0088cc',
        secondary: '#1c242f',
        accent: '#f39c12',
        success: '#27ae60',
        danger: '#e74c3c',
        telegram: {
          bg: '#1c242f',
          text: '#ffffff',
          hint: '#999999',
          link: '#0088cc',
          button: '#0088cc',
          buttonText: '#ffffff',
          secondary: '#232e3c',
          secondaryText: '#aaaaaa',
        }
      },
      animation: {
        'pulse-fast': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  plugins: [],
}
