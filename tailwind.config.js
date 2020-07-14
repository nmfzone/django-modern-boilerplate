const plugin = require('tailwindcss/plugin')

module.exports = {
  purge: {
    content: [
      './assets/js/*.js',
      './assets/js/*.jsx',
      './assets/js/*.vue',
      './**/*.html',
      './**/*.py'
    ],
    options: {
      whitelistPatterns: [
        /-active$/,
        /-enter$/,
        /-leave-to$/
      ]
    }
  },
  theme: {
    extend: {
      fontFamily: {
        body: [
          'Lato',
          'Arial',
          'sans-serif',
        ]
      },
      fontSize: {
        md: '0.925rem',
      }
    },
  },
  variants: {
    textColor: ['responsive', 'hover', 'focus', 'important'],
    margin: ['responsive', 'important'],
    padding: ['responsive', 'important'],
  },
  plugins: [
    plugin(function({ addVariant }) {
      addVariant('important', ({ container }) => {
        container.walkRules(rule => {
          rule.selector = `.${rule.selector.slice(1)}-impt`
          rule.walkDecls(decl => {
            decl.important = true
          })
        })
      })
    })
  ],
}
