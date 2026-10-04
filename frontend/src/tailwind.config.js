/** @type {import('tailwindcss').Config} */

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      fontFamily: {
        sans: ["DM Sans", "sans-serif"],
        Bricolage: ["Bricolage Grotesque", "sans-serif"],
      },

      keyframes: {
        pulseBtn: {
          "50%": {
            transform: "scale(0.97)",
          },
        },
      },

      animation: {
        pulseBtn: "pulseBtn 1s ease-in-out infinite",
      },
    },
  },

  plugins: [],
};