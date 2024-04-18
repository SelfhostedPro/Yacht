import { z } from 'zod'
const DBUserSchema = z.object({
    id: z.string(),
    role: z.union([z.literal('user'), z.literal('admin')]),
    username: z.string(),
    hashedPassword: z.string()
})
type DBUser = z.infer<typeof DBUserSchema>

export { DBUserSchema, type DBUser }