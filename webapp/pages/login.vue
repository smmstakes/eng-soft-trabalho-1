<template>
    <div class="auth-container">
        <h1>Login</h1>
        <form @submit.prevent="submitLogin">
            <div class="form-group">
                <label>
                    E-mail: *
                </label>
                <input type="email" placeholder="Digite o e-mail cadastrado na plataforma" required />
            </div>

            <div class="form-group">
                <label>Senha: *</label>
                <input type="password" placeholder="Digite a senha de ingresso a plataforma" required />
            </div>

            <Button class="auth-join-button" text="Entrar" mode="black" />
        </form>

        <span class="auth-instruction-text">Não tem uma conta?
            <NuxtLink to="/register">
                <List /> Cadastre-se
            </NuxtLink>
        </span>
    </div>

</template>


<script>
</script>
