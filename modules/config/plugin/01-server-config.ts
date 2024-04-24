// import { checkConfig } from '../utils/lvconfig'
// import { Logger } from '../utils/lvlogger'
import { checkConfig } from "../runtime/server/utils/config"
import fs from 'fs-extra'
// Loading the config on initialization so we can make sure settings are applied on startup.
export default defineNitroPlugin((nitroApp) => {
    Logger.info('initializing config module...', 'config')
    return checkConfig().then(() => {
        Logger.ready('config module initialized.', 'config')
        return;
    })
})