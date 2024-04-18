import { defineNuxtModule, addServerImportsDir, installModule, createResolver } from '@nuxt/kit'
import core from '../notifications'

export default defineNuxtModule({
    meta: { name: 'logging' },
    async setup(options, nuxt) {
        await installModule(core, null, nuxt)
        const resolver = createResolver(import.meta.url)
        addServerImportsDir(resolver.resolve('runtime/server/composables'))
    }
})