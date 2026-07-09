/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Outfit', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      colors: {
        background: "#09090b",
        surface: "#18181b",
        border: "#27272a",
        primary: "#ffffff",
        accent: "#10b981",
        'accent-warm': "#f59e0b",
        danger: "#ef4444",
        'text-primary': "#fafafa",
        'text-secondary': "#a1a1aa",
        cta: "#10b981",
      },
      boxShadow: {
        'glow-accent': '0 0 20px rgba(16, 185, 129, 0.35)',
        'glow-warm': '0 0 20px rgba(245, 158, 11, 0.35)',
      },
    },
  },
  plugins: [],
}
