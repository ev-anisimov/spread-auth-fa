const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [],
  configureWebpack: { devtool: 'source-map' }
})
