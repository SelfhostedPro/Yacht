import { defineNuxtModule, addImportsDir, addServerImportsDir, addServerPlugin, installModule, createResolver } from '@nuxt/kit'
import config from '../config'

export default defineNuxtModule({
    meta: { name: 'db' },
    async setup(options, nuxt) {
        await installModule(config, null, nuxt)
        const resolver = createResolver(import.meta.url)
        addImportsDir(resolver.resolve('types'))
        addServerImportsDir(resolver.resolve('runtime/server/utils'))
        // addServerPlugin(resolver.resolve('plugin/02-server-db.ts'))
    }
})