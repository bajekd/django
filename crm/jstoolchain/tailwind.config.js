module.exports = {
  purge: {
    enabled: true,
    content: [
      '../templates/**/*.html',
      '../agents/templates/**/*.html',
      '../arenas/templates/**/*.html',
      '../leads/templates/**/*.html',
    ],
    options: {
      safelist: [
        'bg-green-50',
        'border-green-400',
        'bg-blue-50', 
        'border-blue-400',
        'g-yellow-50',
        'border-yellow-400',
        'bg-red-50',
        'border-red-400',
        'text-green-700',
        'text-blue-700',
        'text-yellow-700',
        'text-red-700'
      ]
    }
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: { 
    extend: {},
  },
  plugins: [],
}