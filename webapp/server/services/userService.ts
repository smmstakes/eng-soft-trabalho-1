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

export const registerUser = async (user: UserData): Promise<UserResponse> => {
  try {
    const res = await api.post('/usuarios/', user)
    return res.data as UserResponse
  } catch (error: any) {
    console.error('Erro ao registrar usuário:', error)

    // Backend Flask retorna sempre um campo "erro" em caso de falha
    if (error.response?.data?.erro) {
      throw new Error(error.response.data.erro)
    }

    // Fallback genérico para erro de rede ou outros
    throw new Error('Erro inesperado ao cadastrar usuário.')
  }
}
