<template>
  <div class="container">
    <TopBar />

    <Header title="Meus Projetos" description="Gerencie e acompanhe seus projetos de eventos">
      <Button @click="showJoinModal = true" text="➜ Ingressar em um Projeto" mode="black" />
      <Button @click="showCreateModal = true" text="+ Novo Projeto" mode="black" />
    </Header>

    <!-- Grid de Projetos -->
    <div class="projects-grid">
      <ProjectCard v-for="project in projects" :key="project.projectId" :id="project.id" :icon="getIcon(project.name)"
        :title="project.name" :description="project.description" :project-id="project.projectId"
        @click="selectProject(project)" />
    </div>

    <!-- Modal Criar Projeto -->
    <Modal title="Criar Projeto" v-model:show="showCreateModal">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label>Título do Projeto *</label>
          <input v-model="form.titulo_projeto" type="text" placeholder="Digite o título" required />
        </div>

        <div class="form-group">
          <label>Descrição do Projeto *</label>
          <textarea v-model="form.descricao" placeholder="Digite a descrição" required />
        </div>

        <div class="form-group">
          <label>CPF *</label>
          <input v-model="form.cpf" type="text" placeholder="Digite seu CPF" required />
        </div>

        <Button text="Criar" mode="black" type="submit" />
      </form>
    </Modal>


    <!-- Modal Ingressar em Projeto -->
    <Modal title="Ingressar em um Projeto" v-model:show="showJoinModal">
      <form @submit.prevent="submitJoinForm">
        <div class="form-group">
          <label>
            ID do Projeto
            <Tooltip text="Os membros da sua equipe usarão essa senha para ingressar no projeto." />
          </label>
          <input v-model="joinForm.projectId" type="text" placeholder="Digite o ID do projeto" required />
        </div>

        <div class="form-group">
          <label>Senha de ingresso *</label>
          <input v-model="joinForm.password" type="password" placeholder="Digite a senha" required />
        </div>

        <div v-if="joinError" class="error">{{ joinError }}</div>

        <Button text="Ingressar" mode="black" type="submit" />
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProject, useProjectsList } from '@/composables/useProject'
import { criarProjeto, ProjetoData, listarProjetos, ProjetoResponse } from '@/server/services/projectService'
import { useToasts } from '@/composables/useToast'

const projects = useProjectsList() // lista global
const currentProject = useProject() // state do projeto selecionado

const showCreateModal = ref(false)
const showJoinModal = ref(false)

const router = useRouter()
const toast = useToasts()

// Formulário de criar projeto
const form = ref<ProjetoData>({
  titulo_projeto: '',
  descricao: '',
  cpf: ''
})

// Formulário de ingressar projeto
const joinForm = ref({
  projectId: '',
  password: ''
})

// Criar projeto
const submitForm = async () => {
  try {
    const projetoCriado = await criarProjeto(form.value)
    projects.value.push(projetoCriado)
    showCreateModal.value = false
    form.value = { titulo_projeto: '', descricao: '', cpf: '' }
    toast.success('Projeto criado com sucesso!')
  } catch (e: any) {
    toast.error(e.message || 'Erro ao criar projeto')
  }
}

// Ingressar em projeto
const submitJoinForm = async () => {
  try {
    console.log('Ingressar no projeto:', joinForm.value)
    showJoinModal.value = false
    joinForm.value = { projectId: '', password: '' }
    toast.success('Ingressou no projeto com sucesso!')
  } catch (e: any) {
    toast.error(e.message || 'Erro ao ingressar no projeto')
  }
}

// Seleciona projeto e redireciona para configuração
const selectProject = (project: ProjetoResponse) => {
  currentProject.value = project
  router.push('/configuration')
}

// Define ícones para cada projeto
function getIcon(name: string) {
  if (name.toLowerCase().includes('shop')) return 'ShoppingBag'
  if (name.toLowerCase().includes('alpha')) return 'Calendar'
  return 'FolderKanban'
}

</script>

<style scoped>
.projects-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 24px;
  padding: 12px 5%;
}

.error {
  color: #ff4d4f;
  /* vermelho forte */
  font-weight: 500;
  background-color: #fff1f0;
  /* leve fundo para destacar */
  padding: 6px 10px;
  border-radius: 4px;
  margin-top: 8px;
  font-size: 0.95rem;
}
</style>
