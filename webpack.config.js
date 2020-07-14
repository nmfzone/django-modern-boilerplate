const mix = require('laravel-mix')
const path = require('path')
const root = path.resolve(__dirname)


/*
 |--------------------------------------------------------------------------
 | Extended Mix Configuration
 |--------------------------------------------------------------------------
 |
 | Here we define our custom Configuration.
 |
 */

const webpackConfig = {
  resolve: {
    symlinks: false,
    alias: {
      '@root': `${root}/assets/js`
    }
  }
}

mix.setPublicPath('./public/static')
   .setResourceRoot(process.env.STATIC_URL)
   .webpackConfig(webpackConfig)

module.exports = webpackConfig
