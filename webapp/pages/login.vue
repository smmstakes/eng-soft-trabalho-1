<template>
  <div class="auth-container">
    <h1>Login</h1>

    <form @submit.prevent="submitLogin">
      <!-- CPF -->
      <div class="form-group">
        <label>CPF: *</label>
        <input
          v-model="credentials.cpf"
          type="text"
          placeholder="Digite seu CPF (000.000.000-00)"
          :class="{ 'input-error': cpfError }"
          required
        />
        <p v-if="cpfError" class="error-text">{{ cpfError }}</p>
      </div>

      <!-- Senha -->
      <div class="form-group">
        <label>Senha: *</label>
        <input
          v-model="credentials.senha"
          type="password"
          placeholder="Digite sua senha"
          :class="{ 'input-error': senhaError }"
          required
        />
        <p v-if="senhaError" class="error-text">{{ senhaError }}</p>
      </div>

      <Button
        class="auth-join-button"
        text="Entrar"
        mode="black"
        type="submit"
      />
    </form>

    <span class="auth-instruction-text">
      Não tem uma conta?
      <NuxtLink to="/register">Cadastre-se</NuxtLink>
    </span>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import { loginUser } from '@/server/services/userService'
import { useRouter } from 'vue-router'
import { setAuth } from '@/composables/useAuth'

// composables e libs
const toast = useToast()
const router = useRouter()

// estado do formulário
const credentials = ref({
  cpf: '',
  senha: ''
})

const cpfError = ref('')
const senhaError = ref('')

// Regex de CPF válido (com pontos e traço)
const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/

// Validação simples e mensurável
const validate = () => {
  let valid = true
  cpfError.value = ''
  senhaError.value = ''

  if (!cpfRegex.test(credentials.value.cpf)) {
    cpfError.value = 'CPF inválido. Use o formato 000.000.000-00.'
    valid = false
  }

  if (credentials.value.senha.length < 4) {
    senhaError.value = 'A senha deve ter pelo menos 4 caracteres.'
    valid = false
  }

  return valid
}

const submitLogin = async () => {
  if (!validate()) {
    toast.error('Preencha os campos corretamente antes de continuar.')
    return
  }

  try {
    console.log('Tentando login com:', credentials.value)
    const res = await loginUser(credentials.value)

    setAuth(res.access_token, {
      cpf: res.cpf,
      nome: res.nome,
      email: res.email
    })

    toast.success('Login realizado com sucesso!')
    router.push('/projects')
  } catch (e: any) {
    console.error('Erro ao fazer login:', e)
    toast.error(e.message)
  }
}
</script>

<style scoped>

</style>
