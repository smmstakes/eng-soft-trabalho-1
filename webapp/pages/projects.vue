<template>
  <div class="container">
    <TopBar />

    <Header title="Meus Projetos" description="Gerencie e acompanhe seus projetos de eventos">
      <Button @click="showJoinModal = true" text="➜ Ingressar em um Projeto" mode="black" />
      <Button @click="showCreateModal = true" text="+ Novo Projeto" mode="black" />
    </Header>

    <div v-if="projects.length === 0" class="empty-state">
      <p>Ainda não há nada por aqui...</p>
      <p>Comece criando um novo projeto ou ingressando em um.</p>
    </div>

    <!-- Grid de Projetos -->
    <div v-else class="projects-grid">
      <ProjectCard v-for="project in projects" :key="project.id" :id="project.id"
        :icon="getIcon(project.titulo_projeto)" :title="project.titulo_projeto" :description="project.descricao"
        @click="selectProject(project)" />
    </div>

    <!-- Modal Criar Projeto -->
    <Modal title="Criar Projeto" v-model:show="showCreateModal">
      <form @submit.prevent="submitCreateProject">
        <div class="form-group">
          <label>Título do Projeto *</label>
          <input v-model="form.titulo_projeto" type="text" placeholder="Digite o título" required />
        </div>

        <div class="form-group">
          <label>Descrição do Projeto *</label>
          <textarea v-model="form.descricao" placeholder="Digite a descrição" required />
        </div>

        <div class="form-group">
          <label>Senha do Projeto *</label>
          <input v-model="form.senha" type="password" placeholder="Crie uma senha para o projeto" required />
        </div>

        <Button text="Criar" mode="black" type="submit" />
      </form>
    </Modal>

    <!-- Modal Ingressar em Projeto -->
    <Modal title="Ingressar em um Projeto" v-model:show="showJoinModal">
      <form @submit.prevent="submitJoinProject">
        <div class="form-group">
          <label>ID do Projeto *</label>
          <input v-model="joinForm.id_projeto" type="number" placeholder="Digite o ID do projeto" required />
        </div>

        <div class="form-group">
          <label>Senha *</label>
          <input v-model="joinForm.senha" type="password" placeholder="Digite a senha do projeto" required />
        </div>

        <div v-if="joinError" class="error">{{ joinError }}</div>

        <Button text="Ingressar" mode="black" type="submit" />
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useProject, useProjectsList } from '@/composables/useProject'
import { listarProjetos, criarProjeto, entrarProjeto } from '@/server/services/projectService'
import { useToasts } from '@/composables/useToast'

const toast = useToasts()
const auth = useAuth()

const ready = ref(false)
const projects = useProjectsList()
const currentProject = useProject()

const showCreateModal = ref(false)
const showJoinModal = ref(false)
const joinError = ref('')

const form = ref({ titulo_projeto: '', descricao: '', senha: '' })
const joinForm = ref({ id_projeto: '', senha: '', cargo: 'Desenvolvedor' })

onMounted(async () => {
  if (!auth.value.token) return navigateTo('/login')

  ready.value = true

  try {
    const data = await listarProjetos(auth.value.token!)
    projects.value = Array.isArray(data) ? data : []
  } catch (e: any) {
    toast.error(e.message || 'Erro ao listar projetos')
  }
})

const submitCreateProject = async () => {
  try {
    const novo = await criarProjeto(form.value, auth.value.token!)
    projects.value.push(novo)
    showCreateModal.value = false
    form.value = { titulo_projeto: '', descricao: '', senha: '' }
    toast.success('Projeto criado com sucesso!')
  } catch (e: any) {
    toast.error(e.message || 'Erro ao criar projeto')
  }
}

const submitJoinProject = async () => {
  try {
    await entrarProjeto(joinForm.value, auth.value.token!)
    showJoinModal.value = false
    joinForm.value = { id_projeto: '', senha: '', cargo: 'Desenvolvedor' }
    toast.success('Ingressou no projeto com sucesso!')
  } catch (e: any) {
    joinError.value = e.message || 'Erro ao ingressar no projeto'
    toast.error(joinError.value)
  }
}

const selectProject = (project: any) => {
  currentProject.value = project
  navigateTo('/configuration')
}

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

.empty-state p {
  text-align: left;
  font-style: normal;
  font-weight: 400;
  font-size: 30px;
  line-height: 30px;

  color: #525252;
}

.error {
  color: #ff4d4f;
  background-color: #fff1f0;
  padding: 6px 10px;
  border-radius: 4px;
  margin-top: 8px;
  font-size: 0.95rem;
}
</style>
