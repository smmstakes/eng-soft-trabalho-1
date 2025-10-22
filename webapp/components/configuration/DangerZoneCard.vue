<template>
  <div class="danger-zone-card">

    <div class="card-content">
      <h3>Zona de Perigo</h3>

      <div>
        <h4>Deletar Projeto</h4>
        <p>Esta ação não pode ser desfeita. Todos os dados serão perdidos</p>
      </div>

    </div>

    <Button @click="openConfirmationModal" class="delete-button" text="Deletar"/>

    <ConfirmModal 
      :show="isModalVisible"
      title="Deletar este projeto?"
      :message="`Você está prestes a deletar o projeto '${project?.name}'. Todos os dados, membros e configurações serão perdidos permanentemente.`"
      @confirm="handleDeleteConfirm"
      @cancel="closeConfirmationModal"
    />
    
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const project = useProject();
const router = useRouter();
const toasts = useToasts();

const isModalVisible = ref(false);

const openConfirmationModal = () => {
  isModalVisible.value = true;
};

const closeConfirmationModal = () => {
  isModalVisible.value = false;
};

const handleDeleteConfirm = async () => {
  if (!project.value) {
    toasts.error('Nenhum projeto selecionado para deletar.');
    return;
  }
  
  try {
    await $fetch(`/api/projects/${project.value.id}`, {
      method: 'DELETE',
    });

    toasts.success(`Projeto "${project.value.name}" deletado com sucesso!`);
    router.push('/homePage'); 
    
    // Limpar o estado após o redirecionamento.
    // Recarregar a lista de projetos na página para onde for redirecionado.

  } catch (error) {
    toasts.error("Não foi possível deletar o projeto.");

  } finally {
    closeConfirmationModal();
  }
};
</script>

<style scoped>
.danger-zone-card {
  border: 1px solid #ef4444;
  background-color: #fef2f2;
  border-radius: 8px;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 964px;
}

.card-content h3 {
  margin-top: 0;
  font-size: large;
  font-weight: 600;
  color: #991b1b;
}

.card-content h4 {
  font-size: medium;
  font-weight: 600;
  margin: 12px 0 4px;
  color: #171717;
}

.card-content p {
  margin: 0;
  color: #52525b;
  font-size: small;
}
</style>
