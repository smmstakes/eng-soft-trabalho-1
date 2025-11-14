<template>
	<div class="backlog-card" @click="$emit('itemClicked', item)">
		<span :class="['priority-tag', priorityClass]">{{ item.prioridade }} Prioridade</span>

		<h3 class="card-title">{{ item.titulo }}</h3>

		<p class="card-text">
			<strong>Objective:</strong> {{ item.objetivo }}
		</p>

		<p class="card-text">
			{{ item.beneficios }}
		</p>
	</div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { BacklogItem } from '@/composables/useBacklog';

defineEmits(['itemClicked']);

const props = defineProps<{
	item: BacklogItem
}>();

const priorityClass = computed(() => {
	switch (props.item.prioridade) {
		case 'Alta': return 'priority-high';
		case 'Média': return 'priority-medium';
		case 'Baixa': return 'priority-low';
		default: return '';
	}
});
</script>

<style scoped>
.backlog-card {
	background-color: #FFFFFF;
	border: 1px solid #E5E7EB;
	border-radius: 8px;
	padding: 24px;
	margin-bottom: 16px;
	box-shadow: 0 2px 4px #0000000d;

	cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.backlog-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px #00000014;
}

.card-title {
	font-size: x-large;
	font-weight: 500;
	margin-top: 16px;
	margin-bottom: 8px;
	color: #171717;
}

.card-text {
	font-size: 1rem;
	color: #374151;
	line-height: 1.5;
	margin-bottom: 12px;
}

.card-text strong {
	font-weight: 600;
	color: #111827;
}

.priority-tag {
	display: inline-block;
	font-size: 0.875rem;
	font-weight: 500;
	padding: 4px 12px;
	border-radius: 9999px;
	text-transform: capitalize;
}

.priority-high {
	background-color: #FEE2E2;
	color: #B91C1C;
}

.priority-medium {
	background-color: #FEF3C7;
	color: #B45309;
}

.priority-low {
	background-color: #D1FAE5;
	color: #065F46;
}
</style>
