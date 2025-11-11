import { initAuth } from '@/composables/useAuth'

export default defineNuxtPlugin(() => {
  initAuth()
})
