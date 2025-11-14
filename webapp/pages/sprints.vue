<template>
  <div class="main-wrapper">
    <!-- Header -->
    <Header title="Sprints" description="Gerencie e acompanhe o progresso das suas sprints">
      <Button @click="showCreateModal = true" text="+ Criar Nova Sprint" mode="black" />
    </Header>

    <!-- Lista de Sprints -->
    <div class="main-content">
      <template v-if="sprints.length > 0">
        <div class="mt-8" v-for="sprint in sprints" :key="sprint.id">
          <SprintCard
            :sprint="{
              id: sprint.id_sprint,
              titulo: sprint.id_sprint,
              inicio: sprint.inicio,
              termino: sprint.termino,
              meta: sprint.meta || []
            }"
          />
        </div>
      </template>

      <div class="mt-8 empty-state" v-else>
        <p>Ainda não tem nada por aqui.<br>
           Comece criando uma sprint!
        </p>
      </div>
    </div>

    <!-- Modal de criação -->
    <Modal title="Criar Sprint" v-model:show="showCreateModal">
      <form @submit.prevent="submitCreateSprint">
        <!-- <div class="form-group">
          <label>Título *</label>
          <input v-model="form.meta" type="text" placeholder="Digite o título" required />
        </div> -->

        <div class="form-group">
          <label>Meta *</label>
          <input v-model="form.meta_sprint" type="text" placeholder="Digite a meta da sprint" required />
        </div>

        <div class="form-group date-row">
          <div>
            <label>Data de Início *</label>
            <input v-model="form.inicio" type="date" required />
          </div>
          <div>
            <label>Data de Término</label>
            <input v-model="form.termino" type="date" />
          </div>
        </div>

        <div class="form-group">
          <label>Revisão da Sprint</label>
          <textarea v-model="form.revisao_sprint" placeholder="Digite a revisão"></textarea>
        </div>

        <Button text="Criar" mode="black" type="submit" />
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useProject, useProjectSprints } from '@/composables/useProject';
import { useAuth } from '@/composables/useAuth';
import { criarSprint, listarSprintsDoProjeto } from '@/server/services/projectService';
import { useToast } from 'vue-toastification';

definePageMeta({ layout: 'config' });

const project = useProject();
const sprints = ref(useProjectSprints() || []);
if (!sprints.value) sprints.value = [];

const auth = useAuth();
const toast = useToast();
const showCreateModal = ref(false);

const form = ref({
  meta: '',
  meta_sprint: '',
  inicio: '',
  termino: '',
  revisao_sprint: ''
});

const submitCreateSprint = async () => {
  if (!project.value) return toast.error("Projeto não definido");
  if (!auth.value.token) return toast.error("Usuário não autenticado");

  try {
    const novaSprint = await criarSprint(project.value.id_projeto, form.value, auth.value.token);
    sprints.value.push(novaSprint);

    form.value = { meta: '', meta_sprint: '', inicio: '', termino: '', revisao_sprint: '' };
    showCreateModal.value = false;
    toast.success("Sprint criada com sucesso!");
  } catch (err: any) {
    console.error(err);
    toast.error(err.message || 'Erro ao criar sprint');
  }
};

// Carregar sprints ao montar o componente
onMounted(async () => {
  console.log(sprints.value)
  if (project.value && auth.value.token) {
    try {
      const data = await listarSprintsDoProjeto(project.value.id_projeto, auth.value.token);
      sprints.value = data || [];
    } catch (err: any) {
      sprints.value = [];
      toast.error('Erro ao carregar sprints. Tente logar novamente.');
    }
  }
});
</script>


<style scoped>
.mt-8 {
  margin-top: 24px;
}

.main-content {
  padding: 20px 32px;
}

.main-content p {
  font-size: 1rem;
  color: #6b7280;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 4px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
  font-size: 1rem;
}

.date-row {
  display: flex;
  gap: 16px;
}

.date-row div {
  flex: 1;
}

.empty-state p {
  text-align: left;
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 30px;
  color: #525252;
}

.main-content {
  padding: 20px 35px;
}
</style>
