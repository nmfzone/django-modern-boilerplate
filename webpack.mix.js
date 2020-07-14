const mix = require('laravel-mix')
require('./webpack.config')
require('laravel-mix-copy-watched')
require('laravel-mix-tailwind')


/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your application.
 |
 */

mix.sass('assets/sass/app.scss', 'css')
   .sass('assets/sass/dashboard.scss', 'css')
   .js('assets/js/app.js', 'js')
   .js('assets/js/dashboard.js', 'js')
   .tailwind('./tailwind.config.js')

mix.extract(['jquery'], 'js/vendor/jquery.js')
   .extract(['vue'], 'js/vendor/vue.js')
   .extract([
     'axios',
     'lodash',
   ], 'js/vendor/common.js')

mix.browserSync({
    proxy: process.env.APP_URL,
    files: ['./']
  })

if (mix.inProduction()) {
  mix.version()
}
