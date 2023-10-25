const colors = require('tailwindcss/colors');

module.exports = {
  purge: {
    enabled: false,
    content: ['../templates/**/*.html', '../accounts/templates/**/*.html'],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'teal-one': '#4cb4c7',
        'teal-two': '#7abecc',
        'teal-three': '#7CD1C0',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
