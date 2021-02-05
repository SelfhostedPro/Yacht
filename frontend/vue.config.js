module.exports = {
  publicPath: "",
  transpileDependencies: ["vuetify"],
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        timeout: 6000,
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          "^/api": ""
        },
        logLevel: "debug"
      }
    }
  }
};
