<template>
    <div class="container">
        <TopBar />
        <Header class="header" title="Meus Projetos" description="Gerencie e acompanhe seus projetos de eventos">
            <Button  @click="showJoinModal = true" text="➜ Ingressar em um Projeto" mode="black" />
            <Button  @click="showCreateModal = true" text="+ Novo Projeto" mode="black" />
        </Header>

        <div class="projects-grid">
            <ProjectCard v-for="project in projects" :key="project.projectId" :icon="getIcon(project.name)"
                :title="project.name" :description="project.description" :project-id="project.projectId" />
        </div>

        <Modal title="Criar Projeto" v-model:show="showCreateModal">
            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label>Título do Projeto *</label>
                    <input type="text" placeholder="Digite seu nome" required />
                </div>

                <div class="form-group">
                    <label>Descrição do Projeto *</label>
                    <textarea type="email" placeholder="Digite seu email" required />
                </div>

                <div class="form-group">
                    <label>Senha de ingresso ao projeto *</label>
                    <input type="password" placeholder="Digite a senha de ingresso ao projeto" required />
                </div>

                <Button text="Criar" mode="black" />
            </form>
        </Modal>

        <Modal title="Ingressar em um Projeto" v-model:show="showJoinModal">
            <form @submit.prevent="submitJoinForm">
                <div class="form-group">
                    <label>
                        ID do Projeto
                        <Tooltip text="Os membros da sua equipe utilizarão essa senha para ingressar no projeto." />
                    </label>
                    <input type="text" placeholder="Digite o ID do projeto" required />
                </div>

                <div class="form-group">
                    <label>Senha de ingresso ao projeto *</label>
                    <input type="password" placeholder="Digite a senha de ingresso ao projeto" required />
                </div>

                <Button text="Ingressar" mode="black" />
            </form>
        </Modal>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'

const projects = ref([])
const showCreateModal = ref(false)
const showJoinModal = ref(false)

onMounted(async () => {
    const res = await fetch('/api/projects')
    projects.value = await res.json()
})

function getIcon(name) {
    // opcional: muda o ícone conforme o nome do projeto
    if (name.toLowerCase().includes('shop')) return 'ShoppingBag'
    if (name.toLowerCase().includes('alpha')) return 'Calendar'
    return 'FolderKanban'
}
</script>

<style scoped>
.projects-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    /* 4 colunas fixas */
    gap: 20px;
    margin-top: 24px;
    padding: 12px 5%;

}

:deep(.header-top) {
    padding: 20px 5%;
    /* sobrescreve o padding interno */
}
</style>
