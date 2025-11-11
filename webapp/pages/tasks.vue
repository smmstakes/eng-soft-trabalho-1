<template>
  <div class="main-wrapper">
    <!-- Header -->
    <Header title="Kanban" :description="headerDescription">
      <Button 
        text="+ Criar Tarefa" 
        mode="black" 
        :disabled="!activeSprint"
        @click="showCreateTaskModal = true"
      />
    </Header>

    <!-- Conteúdo principal -->
    <div class="main-content">
      <!-- Estado vazio -->
      <div class="mt-8 empty-state" v-if="!activeSprint">
        <p>
          Nenhuma sprint ativa encontrada.<br>
          Crie uma sprint para começar a gerenciar tarefas!
        </p>
      </div>

      <!-- Quadro Kanban (vazio por enquanto) -->
      <div class="kanban-board" v-else>
        <!-- Aqui você vai preencher o quadro Kanban depois -->
      </div>
    </div>

    <!-- Modal de criação de tarefa (placeholder) -->
    <Modal title="Criar Tarefa" v-model:show="showCreateTaskModal">
      <p>A implementação do formulário de criação de tarefa vai aqui.</p>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useProject, useProjectSprints } from '@/composables/useProject';
import { useAuth } from '@/composables/useAuth';
import { listarSprintsDoProjeto } from '@/server/services/projectService';

definePageMeta({ layout: 'config' });

const project = useProject();
const sprints = useProjectSprints();
const auth = useAuth();

// Garantir que seja um array
if (!sprints.value) sprints.value = [];

// Computed: retorna a sprint ativa, se houver
const activeSprint = computed(() => {
  return sprints.value.find(sprint => sprint.status === 'em andamento');
});

// Computed: description dinâmica para o Header
const headerDescription = computed(() => {
  if (!activeSprint.value) {
    return "";
  }
  return `Sprint ${activeSprint.value.id} - ${activeSprint.value.meta || activeSprint.value.titulo}`;
});

// Modal de criação de tarefa
const showCreateTaskModal = ref(false);

// Carregar sprints ao montar o componente
onMounted(async () => {
  if (project.value && auth.value.token) {
    try {
      const data = await listarSprintsDoProjeto(project.value.id, auth.value.token);
      sprints.value = data || [];
    } catch (err: any) {
      console.error('Erro ao carregar sprints:', err);
      sprints.value = [];
    }
  }
});
</script>

<style scoped>
.main-content {
  padding: 20px 35px;
}

.empty-state p {
  text-align: left;
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  color: #525252;
}

.kanban-board {
  /* Placeholder vazio para o quadro Kanban */
  min-height: 300px;
  border: 1px dashed #d4d4d8;
  border-radius: 8px;
  margin-top: 24px;
}
</style>
