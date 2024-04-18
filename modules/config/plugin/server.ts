// import { checkConfig } from '../utils/lvconfig'
// import { Logger } from '../utils/lvlogger'
import { checkConfig } from "../runtime/server/utils/config"
// Loading the config on initialization so we can make sure settings are applied on startup.
export default defineNitroPlugin(async (nitroApp) => {
    Logger.info('initializing config module...', 'config')
    await checkConfig()
    Logger.ready('config module initialized.', 'config')
})