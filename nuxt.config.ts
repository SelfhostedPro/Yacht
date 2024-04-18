import { nodePolyfills } from 'vite-plugin-node-polyfills'
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['vuetify-nuxt-module', '@pinia/nuxt', '@vueuse/nuxt', '@vee-validate/nuxt', 'nuxt-monaco-editor', "@formkit/auto-animate"],
  build: {
    transpile: ['vue-sonner', 'vuetify'],
  },
  typescript: {
    typeCheck: true,
    strict: true
  },
  vuetify: {
    moduleOptions: {
      ssrClientHints: {
        reloadOnFirstRequest: true,
        viewportSize: true
      }
    },
  },
  nitro: {
    experimental: {
      openAPI: true
    },
    //@ts-expect-error
    openAPI: {
      meta: {
        title: 'Yacht API',
        // description: 'This might become the next big thing.',
        version: '1.0',
      },
    },
  },
  vite: {
    plugins: [nodePolyfills({ include: ['path'] })]
  }
})