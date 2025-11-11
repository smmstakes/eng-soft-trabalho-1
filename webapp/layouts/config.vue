<template>
	<div class="top-bar">
		<TopBar />
	</div>
		
	<div class="config-layout">
		<Sidebar @projectSelected="handleProjectSelection"/>

			<main class="main-content">
					<slot />
			</main>
	</div>
</template>

<script setup lang="ts">
import { watch } from 'vue';

const members = useProjectMembers();
const projectPassword = useProjectPassword();
const project = useProject();
const projectsList = useProjectsList();


// const { data: fetchedProjects, error } = await useAsyncData('projects', () => $fetch('/api/projects'));

// if (fetchedProjects.value) {
//   projectsList.value = fetchedProjects.value;

//   if (!project.value && projectsList.value.length > 0) {
//     project.value = projectsList.value[0];
//   }
// }


// watch(project, async (newProject) => {
//   if (newProject) {

//     const [fetchedMembers, fetchedPasswordData] = await Promise.all([
//       $fetch(`/api/projects/${newProject.id}/members`),
//       $fetch(`/api/projects/${newProject.id}/password`) // <-- Busca a senha
//     ]);
    
//     members.value = fetchedMembers;
//     projectPassword.value = fetchedPasswordData.password; // <-- Atualiza o estado da senha
//   } else {
//     members.value = [];
//     projectPassword.value = '';
//   }
// }, { immediate: true });


const handleProjectSelection = (selected: Project) => {
  project.value = selected;
};
</script>

<style scoped>
.top-bar {
	max-width: 100%;
}

.config-layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
}
</style>
