module.exports = {
    style: {
        postcss: {
            plugins: [
                require('tailwindcss'),
                require('autoprefixer'),
            ],
        },
    },
    devServer: {
        proxy: {
            "/api": {
                target: "http://localhost:8000",
                timeout: 6000,
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    "/api": ""
                },
                logLevel: "debug"
            }
        }
    }
}