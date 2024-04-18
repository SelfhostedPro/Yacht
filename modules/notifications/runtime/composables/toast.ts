import type { Notification } from '#imports'
import { useNotificationsStore } from '#imports'
import type { Pinia } from 'pinia'
import LVToast from '../components/toast.vue'

// Main function for toasting
export const useLVToast = (pinia: Pinia, { message, dedupe, timeout, level, title }: Notification, options?: any,) => {
    const { $toast } = useNuxtApp()
    // Get notification store with active instance
    const notificationStore = useNotificationsStore(pinia)
    const notifications = storeToRefs(notificationStore)
    // Check recent and active notifications
    const isRecent = notifications.recentNotifications.value.find(n => n.message === message)
    const isActive = notifications.recentNotifications.value.find(n => n.message === message)
    if (isRecent && dedupe === true) {
        console.log(`surpressing duplicate notification: ${level} - ${title} ${message}`)
        return
    } else if (isActive) {
        console.log(`supressing duplicate active notification: ${level} - ${title} ${message}`)
        return
    }
    // Return the toast object to get the toast ID.
    return $toast.custom(markRaw(LVToast), {
        duration: timeout || Number.POSITIVE_INFINITY,
        unstyled: true,
        onAutoClose(toast) {
            notificationStore.removeToast(toast.id, false)
        },
        onDismiss(toast) {
            notificationStore.removeToast(toast.id, false)
            notificationStore.removeToast(toast.id, true)
        },
        componentProps: { title, message, dedupe, timeout, level },
    })
}
