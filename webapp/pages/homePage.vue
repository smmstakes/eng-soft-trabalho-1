<template>
	<div class="main">
		<TopBar />

		<div class="center-text">
			<h1>Olá, {{ name }}</h1>
			<p>Ainda não tem nada por aqui, você gostaria de:</p>

			<div class="choose-mode-buttons">
				<Button @click="showCreateModal = true" text="+ Criar um Projeto" mode="black" />
				<Button @click="showJoinModal = true" text="Ingressar em um Projeto" mode="black" />
			</div>
		</div>

		<Modal title="Criar Projeto" v-model:show="showCreateModal">
			<form @submit.prevent="submitForm">
				<div class="form-group">
					<label>Título do Projeto *</label>
					<input type="text" placeholder="Digite seu nome"required />
				</div>

				<div class="form-group">
					<label>Descrição do Projeto *</label>
					<textarea type="email" placeholder="Digite seu email" required />
				</div>

				<div class="form-group">
					<label>Senha de ingresso ao projeto *</label>
					<input type="password" placeholder="Digite a senha de ingresso ao projeto" required />
				</div>

				<Button text="Criar" mode="black" />
			</form>
		</Modal>

		<Modal title="Ingressar em um Projeto" v-model:show="showJoinModal">
			<form @submit.prevent="submitJoinForm">
				<div class="form-group">
					<label>
						ID do Projeto
						<Tooltip text="Os membros da sua equipe utilizarão essa senha para ingressar no projeto." />
					</label>
					<input type="text" placeholder="Digite o ID do projeto" required />
				</div>

				<div class="form-group">
					<label>Senha de ingresso ao projeto *</label>
					<input type="password" placeholder="Digite a senha de ingresso ao projeto" required />
				</div>

				<Button text="Ingressar" mode="black" />
			</form>
		</Modal>


	</div>
</template>

<script setup>
import { ref } from 'vue'

// TODO: Receber nome vindo da API depois
const name = "Fulano"

const showCreateModal = ref(false)
const showJoinModal = ref(false)
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;

	height: 100vh;
	width: 100%;
}

.center-text {
	display: flex;
	flex-direction: column;
	justify-self: center;
	/* justify-content: center; */
	padding-top: 10%;

	padding-left:20%;
	width: 400px;
	height: 100%;
}

.center-text h1 {
	font-weight: 400;
	font-size: 38px;
	margin: 5px 0px;
}

.center-text p {
	color: #525252;
	font-size: 25px;
	margin: 20px 0px;
}

.choose-mode-buttons {
	display: flex;
	justify-content: space-between;

	width: 100%;
}

.choose-mode-buttons button {
	background-color: #171717;
	color: white;
	font-weight: 400;

	height: 40px;
	padding: 0px 30px;
	border: none;
	border-radius: 6px;
}

.choose-mode-buttons button:hover {
	color: black;
	transition-duration: 500ms;
	background-color: #FFFFFF;
	border: 1px solid #D4D4D4;

	cursor: pointer;
}
</style>
