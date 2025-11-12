<template>
  <div class="kanban-board">
    <KanbanColumn
      v-for="column in columns"
      :key="column.status"
      :title="column.title"
      :tasks="tasksByStatus(column.status)"
      :status="column.status"
      @taskMoved="onTaskMoved"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import KanbanColumn from './KanbanColumn.vue'
import { useTasks } from '@/composables/useTasks'
import { useProjectSprints } from '@/composables/useProject'

const { tasks, carregarTasks, atualizarStatusLocal } = useTasks()
const sprints = useProjectSprints()

const activeSprint = computed(() => {
  const now = new Date()
  return sprints.value.find(s => {
    const inicio = new Date(s.inicio)
    const fim = new Date(s.termino)
    return now >= inicio && now <= fim
  })
})


const columns = [
  { title: 'A Fazer', status: 'todo' },
  { title: 'Em Progresso', status: 'doing' },
  { title: 'Concluído', status: 'done' }
]

const tasksByStatus = (status: string) =>
  tasks.value.filter(t => t.nome_estado === status)

const onTaskMoved = ({ task, toStatus }: any) => {
  atualizarStatusLocal(task.id_task, toStatus)
  // aqui depois podemos chamar PATCH para atualizar no backend
}

onMounted(async () => {
  if (activeSprint.value) {
    await carregarTasks(activeSprint.value.id_sprint)
  }
})
</script>

<style scoped>
.kanban-board {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  padding: 20px 0;
  align-items: flex-start;
}
</style>
