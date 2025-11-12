<template>
  <div class="kanban-column" @dragover.prevent @drop="handleDrop">
    <h3 class="column-title">{{ title }}</h3>
    <hr />
    <div class="task-list">
      <div v-for="task in tasks" :key="task.id" class="task-card" draggable="true" @dragstart="handleDragStart(task)">
        <h4 class="task-title">{{ task.titulo }}</h4>
        <p class="task-desc">{{ task.descricao }}</p>
      </div>

      <div v-if="tasks.length === 0" class="empty-placeholder">
        Nenhuma tarefa
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Task {
  id: number
  titulo: string
  descricao?: string
  status: string
}

const props = defineProps<{
  title: string
  tasks: Task[]
  status: string
}>()

const emit = defineEmits<{
  (e: 'taskMoved', payload: { task: Task; toStatus: string }): void
}>()

const handleDragStart = (task: Task) => {
  event?.dataTransfer?.setData('task', JSON.stringify(task))
}

const handleDrop = (event: DragEvent) => {
  const data = event.dataTransfer?.getData('task')
  if (!data) return

  const task = JSON.parse(data)
  emit('taskMoved', { task, toStatus: props.status })
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
  margin-bottom: 12px;
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
  transition: box-shadow 0.2s;
}

.task-card:active {
  cursor: grabbing;
}

.task-card:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.task-title {
  font-weight: 500;
  font-size: 16px;
  margin: 0 0 4px;
}

.task-desc {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
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
