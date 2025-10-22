<template>
  <div class="password-card">
    <div class="card-header">
      <h2>Senha de Ingresso ao Projeto</h2>
    </div>

    <form @submit.prevent="updatePassword">
      <div class="form-group">
        <label for="accessPassword">Senha de Acesso</label>
        
        <div class="input-with-icon">
            <input 
          id="accessPassword" 
          :type="isPasswordVisible ? 'text' : 'password'" 
          v-model="newPassword" 
          placeholder="Digite a nova senha"
            >
            <button type="button" @click="togglePasswordVisibility" class="toggle-visibility-button">
                <Eye v-if="isPasswordVisible" :size="18" />
                <EyeOff v-else :size="18" />
            </button>
        </div>
        
        <small class="helper-text">Mínimo de 4 caracteres, incluindo números e letras</small>
      </div>

      <div class="alert-info">
        <AlertTriangle :size="18" class="alert-icon"/>
        <span>Esta senha será necessária para novos membros ingressarem no projeto</span>
      </div>

      <div class="form-actions">
        <Button text="Atualizar Senha"/>
      </div>
    </form>

  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { AlertTriangle, Eye, EyeOff } from 'lucide-vue-next';

const project = useProject();
const projectPassword = useProjectPassword();
const toasts = useToasts();
const newPassword = ref('');

const isPasswordVisible = ref(false);

watchEffect(() => {
  newPassword.value = projectPassword.value;
});


const togglePasswordVisibility = () => {
    isPasswordVisible.value = !isPasswordVisible.value;
}


const updatePassword = async () => {
  if (!project.value) {
    toasts.error('Nenhum projeto selecionado.');
    return;
  }
  
  if (newPassword.value.length < 4) {
    toasts.warning('A senha deve ter no mínimo 4 caracteres.');
    return;
  }
  
  try {
    // Faz a chamada PATCH para a API
    await $fetch(`/api/projects/${project.value.id}/password`, {
      method: 'PATCH',
      body: { password: newPassword.value }
    });
    
    // Atualiza o estado global com a nova senha
    projectPassword.value = newPassword.value;
    
    toasts.success('Senha do projeto atualizada com sucesso!');
  } catch (error) {
    toasts.error('Não foi possível atualizar a senha.');
  }
};
</script>

<style scoped>
.password-card {
  background-color: #ffffff;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  max-width: 964px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

h2 {
  font-size: large;
  font-weight: 400;
  color: #171717;
  margin: 0;
}

.project-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px #d4d4d8;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #3f3f46;
}

input[type="text"], input[type="password"]  {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.helper-text {
  font-size: 0.75rem;
  color: #a1a1aa;
  margin-top: 4px;
  display: block;
}

.alert-info {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #f4f4f5;
  border-radius: 6px;
  padding: 12px;
  font-size: 0.875rem;
  color: #3f3f46;
  margin-bottom: 24px;
}

.alert-icon {
  color: #71717a;
  flex-shrink: 0; /* Impede que o ícone seja esmagado */
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.save-button {
  background-color: #171717;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-button:hover {
  background-color: #3f3f46;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon input {
  width: 100%;
  padding: 10px 40px 10px 12px;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

.toggle-visibility-button {
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

.toggle-visibility-button:hover {
  color: #171717;
}
</style>
