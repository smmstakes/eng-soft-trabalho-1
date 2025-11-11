<template>
    <div class="auth-container">
        <h1>Cadastro</h1>
        <form @submit.prevent="submitLogin">
            <div class="form-group">
                <label>
                    CPF: *
                </label>
                <input type="text" placeholder="Digite seu cpf" required />
            </div>

            <div class="form-group">
                <label>
                    Nome: *
                </label>
                <input type="text" placeholder="Digite seu cpf" required />
            </div>

            <div class="form-group">
                <label>
                    E-mail: *
                </label>
                <input type="email" placeholder="Digite o e-mail que deseja cadastrar" required />
            </div>

            <div class="form-group">
                <label>Senha: *</label>
                <input type="password" placeholder="Digite a senha que deseja criar" required />
            </div>

            <Button class="auth-join-button" text="Cadastrar" mode="black" />
        </form>

        <span class="auth-instruction-text">Já tem uma conta? Faça
            <NuxtLink to="/login">
                <List />Login
            </NuxtLink>
        </span>
    </div>

</template>


<script>
</script>
