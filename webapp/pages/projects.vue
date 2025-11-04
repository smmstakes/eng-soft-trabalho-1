<template>
    <div class="container">
        <TopBar />
        <Header class="header" title="Meus Projetos" description="Gerencie e acompanhe seus projetos de eventos">
            <Button text="➜ Ingressar em um Projeto" mode="black" />
            <Button text="+ Novo Projeto" mode="black" />
        </Header>

        <div class="projects-grid">
            <ProjectCard v-for="project in projects" :key="project.projectId" :icon="getIcon(project.name)"
                :title="project.name" :description="project.description" :project-id="project.projectId" />
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'

const projects = ref([])

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
	grid-template-columns: repeat(4, 1fr); /* 4 colunas fixas */
	gap: 20px;
	margin-top: 24px;
	padding: 12px 5%;

}

:deep(.header-top) {
    padding: 20px 5%;
    /* sobrescreve o padding interno */
}
</style>
