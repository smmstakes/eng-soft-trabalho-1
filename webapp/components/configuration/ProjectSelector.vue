<template>
	<div class="project-selector" v-if="selectedProject">
		
		<div class="selector-header" @click="toggleDropdown">
			<div class="project-info">
				<span class="project-name">Projeto {{ selectedProject?.titulo_projeto }}</span>
			</div>

			<ChevronDown class="chevron-icon" :class="{ 'is-rotated': isDropdownOpen }" />
		</div>

		<div v-if="isDropdownOpen" class="dropdown-menu">
			<ul class="project-list">
				<li v-for="project in projects"
						:key="project.id"
						@click="onProjectSelect(project)"
				>
						Projeto {{ project.titulo_projeto }}
				</li>
			</ul>
			<a href="/projects/new" class="new-project-button">
				<Plus class="new-project-icon"/>
				<span>Novo projeto</span>
			</a>
		</div>

		<div class="sprint-status">
			<span> {{ selectedProject!.sprintStatus }}</span>
		</div>
	</div>

	<div v-else class="project-name">
		Carregando projeto...
	</div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { ChevronDown, Plus } from 'lucide-vue-next';
import { useProject, useProjectsList, type ProjetoResponse as Project } from '@/composables/useProject';

const projects = useProjectsList();
const selectedProject = useProject();

const emit = defineEmits(['projectSelected']);

const isDropdownOpen = ref(false);
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const onProjectSelect = (project: Project) => {
  selectedProject.value = project; // Atualiza o estado global
  emit('projectSelected', project);
  isDropdownOpen.value = false;
};

// Atualiza o nome exibido quando o projeto selecionado muda
watch(selectedProject, (newProj) => {
  if (newProj) {
	return
  }
});
</script>


<style scoped>
.project-selector {
	position: relative;
	margin-bottom: 24px;
}

.selector-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 4px;
	background-color: #FAFAFA;
	border-radius: 6px;
	cursor: pointer;
	border: 0px solid #e5e5e5;
	transition: background-color 0.2s;
}

.selector-header:hover {
  	background-color: #e5e7eb;
}

.project-name {
	color: #171717;
	font-size: medium;
	font-weight: 500;
}

.chevron-icon {
	color: #464545;
	transition: transform 0.3s ease;
}

.chevron-icon.is-rotated {
  	transform: rotate(180deg);
}

.sprint-status {
	margin-top: 0px;
	padding: 4px;
}

.sprint-status span {
	color: #171717; 
	font-size: small;
	font-weight: 400;
}

.dropdown-menu {
	position: absolute;
	top: 50%; 
	left: 0;
	right: 0;
	margin-top: 4px;
	background-color: #fafafa;
	border: 1px solid #E5E7EB;
	border-radius: 6px;
	box-shadow: 0 4px 6px #0000001a;
	z-index: 1;
	padding: 8px;
}

.project-list {
	list-style: none;
	margin: 0;
	padding: 0;
}

.project-list li {
	padding: 8px 12px;
	border-radius: 8px;
	cursor: pointer;
	color: #171717;
	font-size: 14px;
}

.project-list li:hover {
  	background-color: #eeeeee;
}

.new-project-button {
	display: flex;
	align-items: center;
	gap: 8px;
	width: 90%;
	margin-top: 8px;
	padding: 8px 12px;
	border-top: 2px solid #e5e5e5;
	cursor: pointer;
	color: #171717;
	font-size: 14px;
	text-decoration: none;
}

.new-project-button:hover {
	background-color: #171717;
	border-radius: 8px;
	border-color: #E5E7EB;
	color: #FFFFFF;
	font-weight: 500;
}

.new-project-icon {
	width: 18px;
	height: 18px;
}
</style>
