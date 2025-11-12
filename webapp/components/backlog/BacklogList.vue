<template>
<div>
	<div v-if="!backlogItems || backlogItems.length === 0" class="empty-state">
		<h3>Ainda não tem nada por aqui.</h3>
		<p>Comece adicionando um item ao backlog.</p>
	</div>

	<div v-else class="backlog-grid">
		<BacklogItem
			v-for="item in backlogItems"
			:key="item.id"
			:item="item" 
      @itemClicked="$emit('itemSelected', $event)"
		/>
	</div>
</div>
</template>

<script setup lang="ts">
import { useBacklog } from '@/composables/useBacklog';

defineEmits(['itemSelected']);

const backlogItems = useBacklog();
</script>

<style scoped>
.empty-state {
	text-align: left;
	padding-left: 32px;
	color: #6B7280;
}

.empty-state h3 {
	font-size: x-large;
	font-weight: 500;
	color: #171717;
    margin: 4px;
}

.empty-state p {
	font-size: large;
	margin: 4px
}

.backlog-grid {
	display: grid;
	grid-template-columns: 1fr;
	gap: 16px;
    padding: 0px 32px;
}
</style>
