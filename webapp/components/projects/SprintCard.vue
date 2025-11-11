<template>
  <div class="sprint-list-card">
    <div class="sprint-header">
      <h3>{{ sprint.titulo }}</h3>
      <span class="sprint-status" :class="statusClass(sprint.status)">
        {{ sprint.status || 'Não iniciado' }}
      </span>
    </div>

    <div class="sprint-dates">
      <span>Início: {{ formatDate(sprint.inicio) }}</span>
      <span>Término: {{ formatDate(sprint.termino) }}</span>
    </div>

    <div class="sprint-goals" v-if="sprint.metas && sprint.metas.length">
      <strong>Metas:</strong>
      <ul>
        <li v-for="goal in sprint.metas" :key="goal.id">{{ goal.titulo }}</li>
      </ul>
    </div>

    <div class="sprint-goals" v-else>
      <em>Sem metas cadastradas</em>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

interface Goal {
  id: number | string;
  titulo: string;
}

interface Sprint {
  id: number | string;
  titulo: string;
  status?: string;
  inicio?: string;
  termino?: string;
  metas?: Goal[];
}

const props = defineProps<{
  sprint: Sprint;
}>();

// Converte status para classes CSS
const statusClass = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'em andamento':
      return 'status-running';
    case 'concluida':
      return 'status-completed';
    case 'finalizada':
      return 'status-finished';
    default:
      return '';
  }
};

// Formata datas
const formatDate = (date?: string) => {
  if (!date) return '-';
  return new Date(date).toLocaleDateString('pt-BR');
};
</script>

<style scoped>
.sprint-list-card {
  background-color: #ffffff;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  max-width: 964px;
  margin-bottom: 16px;
}

.sprint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.sprint-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 500;
  color: #171717;
}

.sprint-status {
  font-size: 0.875rem;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 12px;
  color: #fff;
}

.status-running {
  background-color: #facc15; /* amarelo */
  color: #171717;
}

.status-completed {
  background-color: #10b981; /* verde */
}

.status-finished {
  background-color: #6b7280; /* cinza */
}

.sprint-dates {
  font-size: 0.875rem;
  color: #52525b;
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
}

.sprint-goals ul {
  padding-left: 16px;
  margin: 0;
}

.sprint-goals li {
  font-size: 0.875rem;
  color: #3f3f46;
  margin-bottom: 4px;
}
</style>
