import { initDB } from '../runtime/server/utils/db'
// Loading the config on initialization so we can make sure settings are applied on startup.
export default defineNitroPlugin(async (nitroApp) => {
    Logger.info('initializing db module...', 'db')
    await initDB()
    Logger.ready('db module initialized.', 'db')
})