import api from '../api'

export interface UserData {
  cpf: string
  nome: string
  email: string
  senha: string
}

export interface UserResponse {
  cpf: string
  email: string
  nome: string
  access_token: string
}

export interface LoginData {
  email: string
  senha: string
}

export interface LoginResponse {
  access_token: string
  nome: string
  email: string
  cpf: string
}

export const registerUser = async (user: UserData): Promise<UserResponse> => {
  try {
    const res = await api.post('/usuarios/', user)
    return res.data as UserResponse
  } catch (error: any) {
    console.error('Erro ao registrar usuário:', error)

    if (error.response?.data?.erro) {
      throw new Error(error.response.data.erro)
    }

    throw new Error('Erro inesperado ao cadastrar usuário.')
  }
}


export const loginUser = async (data: LoginData): Promise<LoginResponse> => {
  try {
    const res = await api.post('/usuarios/login', data)
    return res.data as LoginResponse
  } catch (error: any) {
    console.error('Erro ao fazer login:', error)

    if (error.response?.data?.erro) {
      throw new Error(error.response.data.erro)
    }

    throw new Error('Erro inesperado ao realizar login.')
  }
}
