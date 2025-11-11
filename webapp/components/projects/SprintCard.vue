<template>
  <div class="sprint-list-card">
    <h2>Sprints do Projeto {{ project.value?.name }}</h2>

    <div class="sprint-item" v-for="sprint in sprints.value" :key="sprint.id">
      <div class="sprint-header">
        <h3>{{ sprint.titulo }}</h3>
        <span class="sprint-status" :class="statusClass(sprint.status)">
          {{ sprint.status }}
        </span>
      </div>

      <div class="sprint-dates">
        <span>Início: {{ formatDate(sprint.inicio) }}</span>
        <span>Término: {{ formatDate(sprint.termino) }}</span>
      </div>

      <div class="sprint-goals" v-if="sprint.metas?.length">
        <strong>Metas:</strong>
        <ul>
          <li v-for="goal in sprint.metas" :key="goal.id">{{ goal.titulo }}</li>
        </ul>
      </div>
    </div>
  </div>


</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useProject, useProjectSprints } from '@/composables/useProject';
import { listarSprintsDoProjeto } from '@/server/services/projectService';
import { useAuth } from '@/composables/useAuth';

const project = useProject();
const sprints = useProjectSprints();
const auth = useAuth();

// Converte status para classes CSS
const statusClass = (status: string) => {
  switch (status.toLowerCase()) {
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

// Carrega sprints do projeto ao montar o componente
onMounted(async () => {
  if (project.value) {
    try {
      const data = await listarSprintsDoProjeto(project.value.id, auth.value.token!);
      sprints.value = data;
    } catch (err: any) {
      console.error('Erro ao carregar sprints:', err);
      sprints.value = [];
    }
  }
});
</script>

<style scoped>
/* mantém o estilo que você já tinha */
.sprint-list-card {
  background-color: #ffffff;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  max-width: 964px;
}

h2 {
  margin: 0 0 16px 0;
  font-weight: 500;
  font-size: 1.25rem;
  color: #171717;
}

.sprint-item {
  border: 1px solid #d4d4d8;
  border-radius: 8px;
  padding: 16px;
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
