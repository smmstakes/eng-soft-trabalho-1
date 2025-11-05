<template>
	<div class="top-bar">
		<div class="app-title">
			<img src="/logo.svg" class="logo" alt="Logo do sistema">
			<h3>Sistema Scrum</h3>
		</div>

		<NuxtLink to="/configuration" class="profile">
			<img :src="profileImage" class="profile-image" alt="Perfil">
		</NuxtLink>
	</div>
</template>

<script>
import { ref } from 'vue'
const profileImage = ref('/logo.svg') // TODO: Receber foto vinda da API depois

</script>

<style scoped>
.top-bar {
	width: 100%;
	height: 65px;
	display: flex;

	align-items: center;
	justify-content: space-between;
	border-bottom: 2.5px solid #E5E5E5;
}

.top-bar .logo {
	margin: 0px 25px;
}

.top-bar h3 {
	font-weight: 400;
}

.top-bar .app-title {
	display: flex;
}

.top-bar .profile {
	width: 40px;
	height: 40px;
	background-color: #4caf50;
	border-radius: 50%;

	margin-right: 25px;
	justify-self: flex-start;
}
</style>
