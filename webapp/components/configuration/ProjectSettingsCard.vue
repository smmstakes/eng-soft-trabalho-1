<template>
  <div class="settings-card" v-if="project">
    <h2>Configurações Básicas</h2>

    <form @submit.prevent="saveChanges">
      <div class="form-group">
        <label for="projectName">Nome do Projeto</label>
        <input id="projectName" type="text" v-model="form.name">
      </div>

      <div class="form-group">
        <label for="projectDescription">Descrição</label>
        <textarea id="projectDescription" rows="3" v-model="form.description"></textarea>
      </div>

      <div class="form-group">
        <label for="projectId">Id do Projeto</label>
        <div class="input-with-icon">
          <input id="projectId" type="text" :value="project.projectId" readonly>
          <button type="button" @click="copyProjectId" class="copy-button">
            <Copy :size="18" />
          </button>
        </div>
      </div>

      <div class="form-actions">
        <Button text="Salvar alterações" mode="black"/>
      </div>
    </form>
  </div>
  <div v-else>
    Carregando configurações...
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { Copy } from 'lucide-vue-next';

const toasts = useToasts();

const project = useProject();

const form = ref({
  name: '',
  description: '',
});

watchEffect(() => {
  if (project.value) {
    form.value.name = project.value.name;
    form.value.description = project.value.description;
  }
});


const copyProjectId = async () => {
  if (!project.value) return;
  try {
    await navigator.clipboard.writeText(project.value.projectId);
    toasts.success('ID do projeto copiado!'); 
  } catch (err) {
    toasts.error('Não foi possível copiar o ID.');
  }
};


const saveChanges = () => {
  if (!project.value) return;

  // Exemplo:
  // await $fetch(`/api/projects/${project.value.id}`, {
  //   method: 'PATCH',
  //   body: form.value
  // });

  toasts.success(`Alterações para o projeto "${form.value.name}" salvas!`);
};
</script>

<style scoped>
.settings-card {
  background-color: #ffffff;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  max-width: 964px;
  
}

h2 {
  font-size: large;
  font-weight: 400;
  color: #171717;
  margin-top: 0;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #171717;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
  color: #3f3f3f;
  font-family: Inter;
  font-size: medium;
  box-sizing: border-box; /* Garante que padding não afete a largura total */
}

textarea {
  resize: vertical;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon input {
  padding-right: 40px;
  background-color: #f4f4f5;
  cursor: default;
  color: #4e4e4e;
}

.copy-button {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #71717a;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.copy-button:hover {
  color: #171717;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}
</style>