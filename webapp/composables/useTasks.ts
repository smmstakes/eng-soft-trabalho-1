import { ref } from 'vue'
import { listarTasks } from '@/server/services/taskService'
import { useAuth } from '@/composables/useAuth'

const tasks = ref<any[]>([])

export function useTasks() {
  const auth = useAuth()

  const carregarTasks = async (id_sprint: number) => {
    if (!auth.value.token) return
    const data = await listarTasks(id_sprint, auth.value.token)
    tasks.value = data || []
  }

  const atualizarStatusLocal = (id_task: number, novoStatus: string) => {
    const task = tasks.value.find(t => t.id_task === id_task)
    if (task) task.nome_estado = novoStatus
  }

  const adicionarTaskLocal = (task: any) => {
    tasks.value.push(task)
  }

  return { tasks, carregarTasks, atualizarStatusLocal, adicionarTaskLocal }
}
