<template>
  <div class="kanban-column" @dragover.prevent @drop="handleDrop">
    <h3 class="column-title">{{ title }}</h3>
    <hr />
    <div class="task-list">
      <div v-for="task in tasks" :key="taskKey(task)" class="task-card" draggable="true"
        @dragstart="handleDragStart($event, task)">
        <div class="task-main">
          <div class="task-title">{{ taskTitle(task) }}</div>
          <div class="task-meta">
            <span class="task-level"> {{ taskLevel(task) }}</span>
            <span class="task-status-badge">{{ taskState(task) }}</span>
          </div>
        </div>

        <div v-if="task.descricao_task || task.descricao" class="task-desc">
          {{ task.descricao_task || task.descricao }}
        </div>
      </div>

      <div v-if="tasks.length === 0" class="empty-placeholder">
        Nenhuma tarefa
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

const props = defineProps<{
  title: string
  tasks: any[] // aceitarmos qualquer shape vindo do backend
  status: string
}>()

const emit = defineEmits<{
  (e: 'taskMoved', payload: { task: any; toStatus: string }): void
}>()

const taskKey = (task: any) => task.id || task.id_task || JSON.stringify(task)

const taskTitle = (task: any) =>
  task.titulo || task.title || task.descricao_task || task.descricao || 'Tarefa sem título'

const taskLevel = (task: any) => task.nivel_task || task.nivel || '—'

const taskState = (task: any) =>
  task.nome_estado || task.nomeEstado || task.status || ''

const handleDragStart = (event: DragEvent, task: any) => {
  // pegar apenas os campos necessários para transportar
  const payload = {
    id_task: task.id_task || task.id,
    nome_estado: task.nome_estado || task.nomeEstado || task.status || null
  }

  event.dataTransfer?.setData('application/json', JSON.stringify(payload))
  // permitir efeito de cópia/move
  event.dataTransfer!.effectAllowed = 'move'
}

const handleDrop = (event: DragEvent) => {
  const data = event.dataTransfer?.getData('application/json')
  if (!data) return
  try {
    const parsed = JSON.parse(data)
    emit('taskMoved', { task: parsed, toStatus: props.status })
  } catch (e) {
    // fallback: tentar data default se houver
    const raw = event.dataTransfer?.getData('task')
    if (raw) {
      const parsed2 = JSON.parse(raw)
      emit('taskMoved', { task: parsed2, toStatus: props.status })
    }
  }
}
</script>

<style scoped>
.kanban-column {
  background: #fafafa;
  border: 1px solid #e4e4e7;
  border-radius: 12px;
  padding: 16px;
  min-width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.column-title {
  font-size: 18px;
  font-weight: 600;
  color: #27272a;
  margin-bottom: 8px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 100px;
}

.task-card {
  background: white;
  border: 1px solid #e4e4e7;
  border-radius: 8px;
  padding: 10px 12px;
  cursor: grab;
  transition: box-shadow 0.15s, transform 0.12s;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-card:active {
  cursor: grabbing;
  transform: translateY(1px);
}

.task-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
}

.task-main {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.task-title {
  font-weight: 600;
  font-size: 14px;
  color: #111827;
}

.task-meta {
  display: flex;
  gap: 8px;
  align-items: center;
}

.task-level {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 999px;
  background: #f3f4f6;
  color: #111827;
}

.task-status-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 999px;
  background: #eef2ff;
  color: #3730a3;
}

.task-desc {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.3;
}

.empty-placeholder {
  text-align: center;
  color: #a1a1aa;
  font-size: 14px;
  padding: 8px;
  border: 1px dashed #e4e4e7;
  border-radius: 8px;
}
</style>
