<template>
	<div class="tooltip-trigger" @mouseenter="show = true" @mouseleave="show = false">
		<img src="/assets/info-icon.svg" alt="info" class="trigger-icon" />

		<transition name="fade">
			<div v-if="show" class="tooltip-top">
				<div class="tooltip-content">
					<img src="/assets/info-icon.svg" alt="info" class="tooltip-icon" />
					<p>{{ text }}</p>
				</div>
			</div>
		</transition>
	</div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
	text: {
		type: String,
		required: true
	}
})

const show = ref(false)
</script>

<style scoped>
.tooltip-trigger {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
}

.trigger-icon {
	width: 18px;
	height: 18px;
	opacity: 0.7;
	transition: opacity 0.2s ease, transform 0.2s ease;
}

.trigger-icon:hover {
	opacity: 1;
	transform: scale(1.05);
}

.tooltip-top {
	position: fixed;
	top: 20px;
	left: 50%;
	transform: translateX(-50%);
	width: 480px;
	height: 83px;
	background-color: #E5E5E5;
	border-radius: 6px;
	box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 9999;
}

.tooltip-content {
	display: flex;
	align-items: center;
	gap: 12px;
	padding: 0 20px;
	color: #1F1F1F;
	font-size: 0.95rem;
	text-align: left;
}

.tooltip-icon {
	width: 20px;
	height: 20px;
	opacity: 0.8;
	flex-shrink: 0;
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
	transform: translateY(-10px);
}
</style>
