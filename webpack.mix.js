let mix = require('webpack-mix').mix;

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your application. By default, we are compiling the Sass
 | file for your application, as well as bundling up your JS files.
 |
 */


mix.setPublicPath(__dirname + '/static');
mix.js('assets/js/app.js', '/')
    .sass('assets/sass/app.scss', '/');
