import { getUsers } from "../../utils/users"
export default eventHandler(async (event) => {
    const existingUsers = (await getUsers()).length > 0
    return {
        auth: event.context.details.auth,
        theme: event.context.details.theme,
        wizard: !existingUsers
    }
})