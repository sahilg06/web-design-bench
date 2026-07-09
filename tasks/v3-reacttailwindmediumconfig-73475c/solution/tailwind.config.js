/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f172a",
        surface: "#1e293b",
        borderc: "#334155",
        primary: "#ffffff",
        accent: "#38bdf8",
        accentWarm: "#818cf8",
        textPrimary: "#f1f5f9",
        textSecondary: "#94a3b8",
        cta: "#38bdf8",
      },
      fontFamily: {
        sans: ['Roboto', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
