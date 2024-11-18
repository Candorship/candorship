const plugin = require('tailwindcss/plugin')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    fontFamily: {
      merriweather: ['Merriweather', 'serif'],
    },
    extend: {
      animation: {
        slide: "slide 9s linear infinite",
      },
      keyframes: {
        slide: {
          "0%": { transform: "translateY(100%)", opacity: 0.1 },
          "15%": { transform: "translateY(0)", opacity: 1 },
          "30%": { transform: "translateY(0)", opacity: 1 },
          "45%": { transform: "translateY(-100%)", opacity: 1 },
          "100%": { transform: "translateY(-100%)", opacity: 0.1 },
        },
      },
      colors: {
        'valencia': {
          '50': '#fdf3f4',
          '100': '#fce4e5',
          '200': '#faced0',
          '300': '#f5acb0',
          '400': '#ed7c82',
          '500': '#de434b',
          '600': '#cd353d',
          '700': '#ac2930',
          '800': '#8e262b',
          '900': '#772529',
          '950': '#400f12',
        },
        'primary': {
          '50': '#f9f5ed',
          '100': '#f0e6d1',
          '200': '#e2cda6',
          '300': '#d2ac72',
          '400': '#c9995c',
          '500': '#b47b3e',
          '600': '#9b6033',
          '700': '#7c482c',
          '800': '#693c2a',
          '900': '#5a3429',
          '950': '#341a14',
        },
        'secondary': {
          '50': '#f7f4fe',
          '100': '#efebfc',
          '200': '#e3dafa',
          '300': '#cebdf5',
          '400': '#b597ee',
          '500': '#9c6de5',
          '600': '#8d4ed9',
          '700': '#7d3cc5',
          '800': '#6932a5',
          '900': '#572a88',
          '950': '#3e1d68', // main colour
        },
      },
    },
  },
  plugins: [
    plugin(function ({ addVariant }) {
      addVariant('htmx-settling', ['&.htmx-settling', '.htmx-settling &'])
      addVariant('htmx-request', ['&.htmx-request', '.htmx-request &'])
      addVariant('htmx-swapping', ['&.htmx-swapping', '.htmx-swapping &'])
      addVariant('htmx-added', ['&.htmx-added', '.htmx-added &'])
    }),
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
}

