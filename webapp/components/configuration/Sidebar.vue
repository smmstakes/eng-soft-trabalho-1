<template>
	<aside class="sidebar">
		<div class="sidebar-header">
			<ProjectSelector
					:projects="projects"
					@projectSelected="$emit('projectSelected', $event)"
			/>
		</div>

		<nav class="sidebar-nav">
			<ul>
				<li>
					<NuxtLink to="/backlog"><List/> Backlog do Produto</NuxtLink>
				</li>

				<li>
					<NuxtLink to="/sprints"><SquareKanban /> Sprints</NuxtLink>
				</li>

				<li>
					<NuxtLink to="/tasks"><ListCheck /> Tarefas</NuxtLink>
				</li>

				<li>
					<NuxtLink to="/configuration"><Settings /> Configurações</NuxtLink>					
				</li>
			</ul>
		</nav>
		
	</aside>
</template>

<script setup lang="ts">
import {List, ListCheck, SquareKanban, Settings} from 'lucide-vue-next';

const projects = useProjectsList();

defineEmits(['projectSelected']);
</script>

<style scoped>
.sidebar {
	position: static;
	left: 0;
	top: 65px;
	height: auto;
	width: 256px;
	z-index: 0;

	background-color: #FAFAFA;
	border-color: #E5E5E5;
	color: #ecf0f1;
	padding: 16px 16px 16px 14px;
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar-nav {
	margin-top: 24px;
}

.sidebar-nav ul {
	list-style: none;
	padding: 0px;
	margin: 0px;
}

.sidebar-nav li a {
	display: flex;
	align-items: center;
	gap: 12px;

	color: #171717;
	font-weight: 400;
	text-decoration: none;

	border-radius: 10px;
	padding: 8px 0px 8px 4px;

	transition: background-color 0.2s;
}

.sidebar-nav li a:hover {
	background-color: #171717;
	border-radius: 10px;
	border-color: #E5E7EB;
	border-width: 2px;

	color: #FFFFFF;
}
</style>
