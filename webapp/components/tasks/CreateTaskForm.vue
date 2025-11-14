<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label>Descrição da Tarefa *</label>
      <textarea v-model="descricao_task" placeholder="Digite o que deve ser feito" required />
    </div>

    <div class="form-group">
      <label>Nível da Tarefa *</label>
      <select v-model="nivel_task" required>
        <option value="Baixo">Baixo</option>
        <option value="Médio">Médio</option>
        <option value="Alto">Alto</option>
      </select>
    </div>

    <div class="form-group">
      <label>Status Inicial *</label>
      <select v-model="nome_estado" required>
        <option value="todo">A Fazer</option>
        <option value="doing">Em Progresso</option>
        <option value="done">Concluído</option>
      </select>
    </div>

    <Button text="Criar Tarefa" mode="black" type="submit" />
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { criarTask } from '@/server/services/taskService'
import { useAuth } from '@/composables/useAuth'
import { useToasts } from '@/composables/useToast'

const props = defineProps<{ idSprint: number }>()
const emit = defineEmits(['created'])

const auth = useAuth()
const toast = useToasts()

const descricao_task = ref('')
const nivel_task = ref('Médio')
const nome_estado = ref('todo')

const handleSubmit = async () => {
  try {
    const novaTask = await criarTask(
      {
        id_sprint: props.idSprint,
        descricao_task: descricao_task.value,
        nivel_task: nivel_task.value,
        nome_estado: nome_estado.value
      },
      auth.value.token!
    )

    emit('created', novaTask)
    toast.success('Tarefa criada com sucesso!')
    descricao_task.value = ''
  } catch (e: any) {
    toast.error(e.message || 'Erro ao criar tarefa')
  }
}
</script>

<style scoped>
.form-group {
  margin-bottom: 14px;
  display: flex;
  flex-direction: column;
}
textarea,
select {
  border: 1px solid #d4d4d8;
  border-radius: 8px;
  padding: 8px;
  font-size: 15px;
}
label {
  margin-bottom: 6px;
  font-weight: 500;
}
</style>
