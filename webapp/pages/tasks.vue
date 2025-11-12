<template>
  <div class="main-wrapper">
    <!-- Header -->
    <Header title="Kanban" :description="headerDescription">
      <Button text="+ Criar Tarefa" mode="black" :disabled="!activeSprint" @click="showCreateTaskModal = true" />
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

      <div class="kanban-board" v-else>
        <KanbanBoard />
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
  if (!sprints.value || sprints.value.length === 0) return null;

  const now = new Date();

  return sprints.value.find(sprint => {
    const inicio = sprint.inicio ? new Date(sprint.inicio) : null;
    const termino = sprint.termino ? new Date(sprint.termino) : null;

    if (!inicio) return false; // sprint sem início não pode estar ativa

    // Se ainda não começou
    if (now < inicio) return false;

    // Se terminou e data de término existe
    if (termino && now > termino) return false;

    // Se já começou e ainda não terminou
    return true;
  }) || null;
});


// Computed: description dinâmica para o Header
const headerDescription = computed(() => {
  if (!activeSprint.value) {
    return "";
  }
  return `Sprint ${activeSprint.value.id_sprint}`;
});

// Modal de criação de tarefa
const showCreateTaskModal = ref(false);

// Carregar sprints ao montar o componente
onMounted(async () => {
  if (project.value && auth.value.token) {
    try {
      const data = await listarSprintsDoProjeto(project.value.id_projeto, auth.value.token);
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

</style>
