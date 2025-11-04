<template>
	<div class="page-header">
		<div class="header-top">
			<div class="header-texts">
				<h1 class="header-title">{{ title }}</h1>
				<h3 class="header-description">{{ description }}</h3>
			</div>

			<!-- Slot opcional para botões, menus, etc -->
			<div class="header-actions">
				<slot />
			</div>
		</div>

		<hr class="header-divider" />
	</div>
</template>

<script setup>
const props = defineProps({
	title: {
		type: String,
		required: true
	},
	description: {
		type: String,
		default: ''
	}
})
</script>

<style scoped>
.page-header {
	display: flex;
	flex-direction: column;
}

.header-top {
	display: flex;
	justify-content: space-between;
	flex-wrap: wrap;
    padding: 20px 36px;
}

.header-texts {
	display: flex;
	flex-direction: column;
}

.header-title {
	color: #171717;
	font-size: x-large;
	font-weight: 500;
	margin: 4px 0;
}

.header-description {
	color: #404040;
	font-size: large;
	font-weight: 400;
	margin: 4px 0;
}

/* Slot — alinha à direita */
.header-actions {
	display: flex;
	align-items: center;
	gap: 8px;
}

/* Linha fina cinza */
.header-divider {
	border: none;
	border-top: 1px solid #D4D4D4;
	margin: 0;
}
</style>
