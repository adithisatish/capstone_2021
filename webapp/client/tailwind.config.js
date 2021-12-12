module.exports = {
  content: [
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {},
    maxWidth: {
      '1/4': '25%',
      '1/2': '50%',
      '3/4': '75%',
      '1/3': '33%'
    },
    screens: {
      'ph': {'max': '1024px'},
      'lg': {'min': '1025px'}
    }
  },
  plugins: [
    require("@tailwindcss/forms")({strategy:"class"})
  ],
}
