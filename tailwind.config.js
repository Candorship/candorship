const plugin = require('tailwindcss/plugin')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    fontFamily: {
      merriweather: ['Merriweather', 'serif'],
    },
  }
}

