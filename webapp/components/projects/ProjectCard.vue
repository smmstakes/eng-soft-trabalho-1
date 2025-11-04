<template>
	<div class="card" @click="goToProject">
		<div class="icon-container">
			<component :is="icon" class="icon" />
		</div>

		<div class="card-body">
			<h3 class="card-title">{{ title }}</h3>
			<p class="card-description">{{ description }}</p>
		</div>
	</div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import * as icons from 'lucide-vue-next'

const props = defineProps({
	icon: {
		type: String,
		default: 'FolderKanban' // ícone padrão
	},
	title: {
		type: String,
		required: true
	},
	description: {
		type: String,
		required: true
	},
	projectId: {
		type: String,
		required: true
	}
})

const router = useRouter()

const goToProject = () => {
	router.push(`/projects/${props.projectId}`)
}

// resolve o componente do ícone dinamicamente
const icon = icons[props.icon] || icons.FolderKanban
</script>

<style scoped>
.card {
	display: flex;
	flex-direction: column;
	border: 1px solid #E5E5E5;
	border-radius: 6px;
	padding: 14px;
	width: 262px;
	height: 180px;
	background-color: #fff;
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
	cursor: pointer;
	transition: box-shadow 0.2s ease, transform 0.1s ease;
}

.card:hover {
	box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
	transform: translateY(-2px);
}

.icon-container {
	width: 48px;
	height: 48px;
	border-radius: 8px;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-bottom: 10px;
}

.icon {
	color: white;
	background-color: #737373;
	border-radius: 4px;
	padding: 6px;
	width: 28px;
	height: 28px;
}

.card-title {
	font-weight: 400;
	font-size: 14pt;
	color: #171717;
	margin: 0 0 4px 0;
}

.card-description {
    margin-top: 10px;
	font-size: 12pt;
	color: #525252;
}
</style>
