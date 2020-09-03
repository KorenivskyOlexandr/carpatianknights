// var path = require('path');
// var webpack = require('webpack');
// var BundleTracker = require('webpack-bundle-tracker');
//
// module.exports = {
//     context: __dirname,
//     entry: './src/js/index',
//     mode: 'development',
//     output: {
//         path: path.resolve('./src/webpack_bundles/'),
//         filename: "[name]-[hash].js"
//     },
//
//     plugins: [
//         new BundleTracker({filename: './webpack-stats.json'})
//     ]
// }

const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: './src/js/index.js',
    mode: 'development',
    output: {
        filename: '../carpatianknights/front_end/static/script/script.js',
    },
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: '../fonts/'
                    }
                }]
            },
            {
                test: /\.(jpe?g|png|gif|svg)(\?[a-z0-9=.]+)?$/,
                use: [{
                    loader: 'url-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: '../images/',
                        limit: 100000,
                    }
                }]

            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '../carpatianknights/front_end/static/css/index.css',
        }),
    ]
};