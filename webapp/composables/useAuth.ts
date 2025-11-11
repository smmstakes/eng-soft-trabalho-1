// composables/useAuth.ts
export interface AuthUser {
  cpf: string
  nome: string
  email: string
}

export interface AuthState {
  token: string | null
  user: AuthUser | null
}

export const useAuth = () =>
  useState<AuthState>('auth', () => ({
    token: process.client ? localStorage.getItem('token') : null,
    user: process.client && localStorage.getItem('user')
      ? JSON.parse(localStorage.getItem('user')!)
      : null
  }))

export const setAuth = (token: string, user: AuthUser) => {
  const auth = useAuth()
  auth.value = { token, user }

  if (process.client) {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
  }
}

export const clearAuth = () => {
  const auth = useAuth()
  auth.value = { token: null, user: null }

  if (process.client) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}
