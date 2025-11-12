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
import { ref, computed } from 'vue'
import KanbanColumn from './KanbanColumn.vue'

interface Task {
  id: number
  titulo: string
  descricao?: string
  status: string
}

// ✅ MOCK inicial — depois você pode buscar do backend via API
const tasks = ref<Task[]>([
  { id: 1, titulo: 'Configurar backend', descricao: 'Criar endpoints', status: 'todo' },
  { id: 2, titulo: 'Montar layout Kanban', descricao: 'UI inicial', status: 'doing' },
  { id: 3, titulo: 'Testar login', descricao: 'Fluxo completo', status: 'done' }
])

const columns = [
  { title: 'A Fazer', status: 'todo' },
  { title: 'Em Progresso', status: 'doing' },
  { title: 'Concluído', status: 'done' }
]

// Computed para filtrar tasks por status
const tasksByStatus = (status: string) => {
  return tasks.value.filter(t => t.status === status)
}

// Handler quando uma task é movida
const onTaskMoved = ({ task, toStatus }: { task: Task; toStatus: string }) => {
  const target = tasks.value.find(t => t.id === task.id)
  if (target) target.status = toStatus
}
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
