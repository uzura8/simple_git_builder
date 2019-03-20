"use strict";
const webpack = require('webpack');
const path = require('path');
const root = path.join(__dirname, './');

const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = [
  {
    devtool: 'source-map',
    entry: {
      index: path.join(root, 'src/js/index.js')
    },
    output: {
      path: path.join(root, 'app/statics/js'),
      filename: '[name].js'
    },
    optimization: {
      splitChunks: {
        name: 'vendor',
        chunks: 'initial'
      },
      minimizer: [
        new TerserPlugin()
      ],
    },
    module: {
      rules: [
        {
          test: /\.vue$/,
          use: [
            {
              loader: 'vue-loader'
            }
          ]
        },
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: [
            {
              loader: 'babel-loader',
              options: {
                presets: [
                  '@babel/preset-env'
                ]
              }
            },
          ]
        },
        {
          test: /\.css$/,
          use: [
            'style-loader',
            {loader: 'css-loader', options: {url: false}}
          ],
        }
      ]
    },
    resolve: {
      modules: [
        path.join(root, '/src'),
        'node_modules'
      ],
      extensions: ['*', '.js', '.vue', '.json'],
      alias: {
        'vue$': 'vue/dist/vue.esm.js',
        'vue-router$': 'vue-router/dist/vue-router.esm.js'
      }
    },
    plugins: [
      new VueLoaderPlugin(),
      // Ignore all locale files of moment.js
      new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    ],
  },
  {
    devtool: 'source-map',
    entry: {
      style: path.join(root, 'src/scss/style.scss')
    },
    output: {
      path: path.join(root, 'app/statics/css'),
      filename: '[name].css'
    },
    module: {
      rules: [
        {
          test: /\.(sa|sc|c)ss$/,
          use: [
            // Output as css file not included js
            MiniCssExtractPlugin.loader,
            {
              loader: 'css-loader',
              options: {
                url: false,
                //minimize: true,
                sourceMap: true
              }
            },
            {
              loader: 'sass-loader',
              options: {
                outputStyle: 'compressed',
                sourceMap: true
              }
            },
            {
              loader: 'postcss-loader',// Setting for PostCSS
              options: {
                plugins: (loader) => [
                  // Enable Autoprefixer
                  // Add vendor prefix
                  require('autoprefixer')({
                    grid: true, // use CSS Grid Layout
                    browsers: ['Android >= 4.4', "IE 11"],
                  })
                ],
                sourceMap: true
              }
            }
          ]
        }
      ]
    },
    plugins: [
      new MiniCssExtractPlugin({
        // prefix is output.path
        filename: '[name].min.css'
      })
    ]
  }
];
