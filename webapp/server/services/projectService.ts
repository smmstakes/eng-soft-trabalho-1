import api from '../api'
import { useAuth } from '@/composables/useAuth'
const auth = useAuth()

export interface ProjetoData {
  titulo_projeto: string
  descricao: string
  senha: string
}

export const listarProjetos = async (token: string) => {
  const res = await api.get('/projetos/', {
    headers: { Authorization: `Bearer ${token}` },
  })
  return res.data
}

export const criarProjeto = async (projeto: ProjetoData, token: string) => {
  const res = await api.post('/projetos/', projeto, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return res.data
}

export const entrarProjeto = async (dados: any, token: string) => {
  const res = await api.post('/projetos/entrar', dados, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return res.data
}
