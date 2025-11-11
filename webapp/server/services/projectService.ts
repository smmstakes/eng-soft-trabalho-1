import api from '../api'
import { useAuth } from '@/composables/useAuth'
const auth = useAuth()

export interface ProjetoData {
  titulo_projeto: string
  descricao: string
  senha: string
}

export interface Sprint {
  id: number
  titulo: string
  descricao?: string
  revisao?: string
  inicio?: string
  termino?: string
  status: 'Em andamento' | 'Concluida' | 'Finalizada'
  metas?: { id: number; titulo: string }[]
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

// **Nova função para listar sprints de um projeto**
export const listarSprintsDoProjeto = async (id_projeto: number, token: string) => {
  const res = await api.get(`/sprints/por-projeto/${id_projeto}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return res.data as Sprint[]
}

export const criarSprint = async (
  id_projeto: number,
  data: { meta: string; inicio: string; termino: string; revisao_sprint: string },
  token: string
) => {
  const payload = {
    id_projeto,
    meta: data.meta,
    inicio: data.inicio,
    termino: data.termino,
    revisao_sprint: data.revisao_sprint
  }

  const res = await api.post('/sprints/', payload, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.data;
}


