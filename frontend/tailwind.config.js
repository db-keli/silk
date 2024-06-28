/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {fontFamily: {sans: ['"Fira Code"', 'monospace',], open: ['"Open Sans"']},},
  },
  plugins: [],
}

