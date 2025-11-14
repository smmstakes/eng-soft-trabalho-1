<template>
<div class="main-wrapper">

  <Header class="header" title="Backlog do Produto" description="Gerencie e acompanhe as user stories do projeto">
    <Button @click="showCreateBacklogModal = true" text="+ Adicionar Item" mode="black" />
  </Header>

  <Modal title="História de Usuário" v-model:show="showCreateBacklogModal">
    <form @submit.prevent="submitCreateForm">
      
      <div class="form-group">
        <label>Título da História de Usuário *</label>
        <input v-model="form.titulo" type="text" placeholder="Digite o título da história de usuário..." required />
      </div>
      
      <div class="form-group">
        <label>Objetivo *</label>
        <textarea v-model="form.objetivo" placeholder="Descreva o objetivo da história de usuário..." required />
      </div>

      <div class="form-group">
        <label>Benefícios</label>
        <textarea v-model="form.beneficios" placeholder="Descreva os benefícios que essa história de usuario irá promover..." />
      </div>

      <div class="form-group">
        <label>Prioridade (Opcional)</label>
        <div class="priority-options">
          
          <input 
            type="radio" 
            id="priority-high" 
            name="priority" 
            v-model="form.prioridade" 
            value="Alta">
          <label for="priority-high" class="priority-label priority-high">
            <span>Alta</span>
          </label>

          <input 
            type="radio" 
            id="priority-medium" 
            name="priority" 
            v-model="form.prioridade" 
            value="Média">
          <label for="priority-medium" class="priority-label priority-medium">
            <span>Média</span>
          </label>

          <input 
            type="radio" 
            id="priority-low" 
            name="priority" 
            v-model="form.prioridade" 
            value="Baixa">
          <label for="priority-low" class="priority-label priority-low">
            <span>Baixa</span>
          </label>

        </div>
      </div>

      <Button text="Criar Item" mode="black" type="submit" />
    </form>
  </Modal>

  <Modal title="Editar Item do Backlog" v-model:show="showEditBacklogModal" v-if="selectedItem">
    <form @submit.prevent="handleUpdateItem">
      
      <div class="form-group">
        <label>Título da User Story *</label>
        <input v-model="editForm.titulo" type="text" required />
      </div>

      <div class="form-group">
        <label>Prioridade *</label>
        <div class="priority-options">
          <input type="radio" id="edit-priority-high" v-model="editForm.prioridade" value="High">
          <label for="edit-priority-high" class="priority-label priority-high">Alta</label>
          
          <input type="radio" id="edit-priority-medium" v-model="editForm.prioridade" value="Medium">
          <label for="edit-priority-medium" class="priority-label priority-medium">Média</label>
          
          <input type="radio" id="edit-priority-low" v-model="editForm.prioridade" value="Low">
          <label for="edit-priority-low" class="priority-label priority-low">Baixa</label>
        </div>
      </div>

      <div class="form-group">
        <label>Objetivo *</label>
        <textarea v-model="editForm.objetivo" required />
      </div>

      <div class="form-group">
        <label>User Story</label>
        <textarea v-model="editForm.beneficios" />
      </div>

      <div class="form-actions">
        <Button text="Salvar Alterações" mode="black" type="submit" />
        
        <Button 
          text="Excluir Item" 
          mode="danger" 
          type="button" 
          @click="executeDelete" />
      </div>

    </form>
  </Modal>

  <ConfirmModal
    v-model:show="showDeleteConfirmModal"
    title="Confirmar Exclusão"
    message="Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita."
    confirmText="Sim, Excluir"
    @confirm="executeDelete" 
  />

  <div class="mt-8">
    <BacklogList @itemSelected="handleItemSelect" />
  </div>

</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useToast } from 'vue-toastification';
import { useProject } from '@/composables/useProject';
import { useBacklog } from '@/composables/useBacklog';
import { criarBacklogItem, atualizarBacklogItem, excluirBacklogItem } from '@/server/services/backlogServices';

import BacklogList from '@/components/backlog/BacklogList.vue';

definePageMeta({
    layout: 'config', 
});

const project = useProject();
const backlogItems = useBacklog();

const showCreateBacklogModal = ref(false);
const toast = useToast();

const form = ref({
  titulo: "",
  objetivo: "",
  beneficios: "",
  prioridade: 'Média'
});

const showEditBacklogModal = ref(false);
const selectedItem = ref<BacklogItem | null>(null);
const showDeleteConfirmModal = ref(false);

const editForm = ref({
  titulo: "",
  objetivo: "",
  beneficios: "",
  prioridade: 'Média' as 'Alta' | 'Média' | 'Baixa'
});


const handleItemSelect = (item: BacklogItem) => {
  selectedItem.value = item;
  
  editForm.value = {
    titulo: item.titulo,
    objetivo: item.objetivo,
    beneficios: item.beneficios,
    prioridade: item.prioridade
  };
  
  showEditBacklogModal.value = true;
};


const handleUpdateItem = async () => {
  if (!selectedItem.value || !project.value) return;

  try {
    const updatedItem = await atualizarBacklogItem(
      project.value.id,
      selectedItem.value.id,
      editForm.value
    );

    const index = backlogItems.value.findIndex(i => i.id === updatedItem.id);
    if (index !== -1) {
      backlogItems.value[index] = updatedItem;
    }

    toast.success('Item atualizado com sucesso!');
    showEditBacklogModal.value = false;
    selectedItem.value = null;

  } catch (e: any) {
    toast.error(e.message || 'Erro ao atualizar item');
  }
};

const executeDelete = async () => {
  if (!selectedItem.value || !project.value) return;

  try {
    await excluirBacklogItem(
      project.value.id,
      selectedItem.value.id
    );

    backlogItems.value = backlogItems.value.filter(
      i => i.id !== selectedItem.value!.id
    );

    toast.success('Item excluído com sucesso!');
    
    showEditBacklogModal.value = false;
    showDeleteConfirmModal.value = false; 
    
    selectedItem.value = null;

  } catch (e: any) {
    toast.error(e.message || 'Erro ao excluir item');
  }
};

const submitCreateForm = async () => {
  if (!project.value) {
    toast.error('Nenhum projeto selecionado. Por favor, selecione um projeto.');
    return;
  }

  try {
    // Junta os dados do formulário com o ID do projeto
    const itemData = {
      ...form.value,
      id_projeto: project.value.id
    };

    const novoItem = await criarBacklogItem(itemData);

    backlogItems.value.push(novoItem);

    showCreateBacklogModal.value = false;
    form.value = { titulo: "", objetivo: "", beneficios: "", prioridade: 'Média' };
    
    toast.success('Item do backlog criado com sucesso!');

  } catch (e: any) {
    toast.error(e.message || 'Erro ao criar item');
  }
}
</script>

<style scoped>
.main-wrapper {
	padding: 0px;
}

.header {
  padding: 0px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  margin-left: 4px;
  font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #E5E7EB;
  border-radius: 6px;
  box-sizing: border-box;
  margin: 2px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
}

.priority-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}

.priority-options input[type="radio"] {
  display: none; 
}

.priority-label {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 9999px;
  border: 2px solid #E5E7EB;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  
  background-color: #FAFAFA;
  color: #6B7280;
}

.priority-label:hover {
  border-color: #D1D5DB;
}

input[type="radio"]:checked + label.priority-high {
  background-color: #FEE2E2; 
  color: #B91C1C; 
  border-color: #FCA5A5;
}

input[type="radio"]:checked + label.priority-medium {
  background-color: #FEF3C7; 
  color: #B45309; 
  border-color: #FCD34D;
}

input[type="radio"]:checked + label.priority-low {
  background-color: #D1FAE5; 
  color: #065F46; 
  border-color: #6EE7B7;
}

.mt-8 {
	margin-top: 32px;
}
</style>