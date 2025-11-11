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
    token: null,
    user: null
  }))

export const initAuth = () => {
  if (process.client) {
    const auth = useAuth()
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('user')

    if (token && user) {
      auth.value = {
        token,
        user: JSON.parse(user)
      }
    }
  }
}

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

export const isAuthenticated = () => {
  const auth = useAuth()
  return !!auth.value.token
}
