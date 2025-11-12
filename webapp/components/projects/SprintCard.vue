<template>
  <div class="sprint-list-card">
    <div class="sprint-header">
      <h3>Sprint {{ sprint.titulo }}</h3>
      <span class="sprint-status" :class="statusClass(calculatedStatus)">
        {{ calculatedStatus }}
      </span>
      <span class="sprint-dates">{{ formatDate(sprint.inicio) }} - {{ formatDate(sprint.termino) }}</span>
    </div>

    <div class="sprint-goals" v-if="sprint.meta">
      <p><span>Meta:</span>{{ sprint.meta }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface Sprint {
  id_sprint: number
  titulo?: string
  descricao?: string
  revisao?: string
  inicio?: string
  termino?: string
  status?: 'Em andamento' | 'Concluida' | 'Finalizada'
  meta?: string
}

const props = defineProps<{
  sprint: Sprint;
}>();

const formatDate = (date?: string) => {
  if (!date) return '-';
  return new Date(date).toLocaleDateString('pt-BR');
};

// Calcula status da sprint dinamicamente com base nas datas
const calculatedStatus = computed(() => {
  if (!props.sprint.inicio) return 'Não iniciado';

  const now = new Date();
  const inicio = new Date(props.sprint.inicio);
  const termino = props.sprint.termino ? new Date(props.sprint.termino) : null;

  if (now < inicio) return 'Não iniciado';
  if (termino && now > termino) return 'Concluída';
  return 'Em andamento';
});

// Classe CSS baseada no status
const statusClass = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'em andamento':
      return 'status-running';
    case 'concluída':
    case 'concluida':
      return 'status-completed';
    case 'não iniciado':
      return 'status-finished';
    default:
      return '';
  }
};
</script>


<style scoped>
.sprint-list-card {
  background-color: #ffffff;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 16px;
}

.sprint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  width: fit-content;
  gap: 12px;
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
  background-color: #E5E7EB;
  color: #262626;
}

.status-completed {
  background-color: #10b981;
}

.status-finished {
  background-color: #6b7280;
}

.sprint-dates {
  margin-left: 20px;
}

.sprint-goals span {
  color: #525252;
  margin-right: 6px;
}

.sprint-goals li {
  font-size: 0.875rem;
  color: #3f3f46;
  margin-bottom: 4px;
}
</style>
