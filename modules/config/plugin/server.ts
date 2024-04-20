// import { checkConfig } from '../utils/lvconfig'
// import { Logger } from '../utils/lvlogger'
import { checkConfig } from "../runtime/server/utils/config"
import fs from 'fs-extra'
// Loading the config on initialization so we can make sure settings are applied on startup.
export default defineNitroPlugin(async (nitroApp) => {
    Logger.info('initializing config module...', 'config')
    fs.ensureDir(useRuntimeConfig().yacht.configOptions.configPath, (err) => {
        if (err) Logger.error(err)
        else Logger.info(`Creating config directory!`, 'config - plugin')
    })
    fs.ensureDir(useRuntimeConfig().yacht.configOptions.dataPath, (err) => {
        if (err) Logger.error(err)
        else Logger.info(`Creating data directory!`, 'config - plugin')
    })
    await checkConfig()
    Logger.ready('config module initialized.', 'config')
})