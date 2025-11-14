import api from '../api'

export interface Task {
  id_task: number
  id_sprint: number
  descricao_task: string
  nivel_task: string
  nome_estado: 'todo' | 'doing' | 'done'
}

export const listarTasks = async (id_sprint: number, token: string) => {
  try {
    const res = await api.get(`/tasks/?id_sprint=${id_sprint}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    return res.data as Task[]

  } catch (error) {
    throw error
  }
}

export const criarTask = async (taskData: any, token: string) => {
  const res = await api.post('/tasks/', taskData, {
    headers: { Authorization: `Bearer ${token}` },
  })
  return res.data
}
