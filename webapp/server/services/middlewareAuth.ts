import { useAuth, initAuth } from '@/composables/useAuth'

export default defineNuxtRouteMiddleware((to) => {
  // inicializa auth (só roda no client)
  initAuth()
  const auth = useAuth()

  const publicPages = ['/login', '/register'] // rotas públicas
  const isPublic = publicPages.includes(to.path)

  // se não estiver autenticado e não for rota pública
  if (!auth.value.token && !isPublic) {
    return navigateTo('/login')
  }

  // se estiver logado e tentar ir pro login ou register
  if (auth.value.token && isPublic) {
    return navigateTo('/projects')
  }
})
