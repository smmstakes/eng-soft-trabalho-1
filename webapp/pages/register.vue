<template>
  <div class="auth-container">
    <h1>Cadastro</h1>

    <form @submit.prevent="submitForm">
      <!-- CPF -->
      <div class="form-group">
        <label>CPF: *</label>
        <input
          v-model="user.cpf"
          type="text"
          placeholder="Digite seu CPF (ex: 123.456.789-00)"
          :class="{ 'input-error': cpfError }"
          required
        />
        <p v-if="cpfError" class="error-text">{{ cpfError }}</p>
      </div>

      <!-- Nome -->
      <div class="form-group">
        <label>Nome: *</label>
        <input
          v-model="user.nome"
          type="text"
          placeholder="Digite seu nome"
          required
        />
      </div>

      <!-- Email -->
      <div class="form-group">
        <label>E-mail: *</label>
        <input
          v-model="user.email"
          type="email"
          placeholder="Digite o e-mail que deseja cadastrar"
          required
        />
      </div>

      <!-- Senha -->
      <div class="form-group">
        <label>Senha: *</label>
        <input
          v-model="user.senha"
          type="password"
          placeholder="Digite a senha que deseja criar"
          required
        />
      </div>

      <Button
        class="auth-join-button"
        text="Cadastrar"
        mode="black"
        type="submit"
      />
    </form>

    <span class="auth-instruction-text">
      Já tem uma conta? Faça
      <NuxtLink to="/login">Login</NuxtLink>
    </span>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { registerUser } from '@/server/services/userService'
import { useToast } from 'vue-toastification'

const toast = useToast()

const user = ref({
  cpf: '',
  nome: '',
  email: '',
  senha: ''
})

const cpfError = ref('')

const cpfRegex = /^\d{3}\.\d{3}\.\d{3}-\d{2}$/

const validateCpf = (cpf) => {
  if (!cpfRegex.test(cpf)) {
    cpfError.value = 'O CPF deve estar no formato 000.000.000-00.'
    return false
  }
  cpfError.value = ''
  return true
}

const submitForm = async () => {
  try {
    if (!validateCpf(user.value.cpf)) {
      toast.error('Corrija o formato do CPF antes de continuar.')
      return
    }
    const res = await registerUser(user.value)

    toast.success('Usuário cadastrado com sucesso!')
  } catch (e) {
    toast.error(e.message)
  }
}
</script>
