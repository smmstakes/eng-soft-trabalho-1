<template>
  <div v-if="show" class="modal-backdrop" @click.self="$emit('cancel')">
    
		<div class="modal-content">
      <h3 class="modal-title">{{ title }}</h3>
      <p class="modal-message">{{ message }}</p>

      <div class="modal-actions">
        <button @click="$emit('cancel')" class="button-secondary">Cancelar</button>
        <button @click="$emit('confirm')" class="button-danger">Confirmar Deleção</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  title: {
    type: String,
    default: 'Você tem certeza?',
  },
  message: {
    type: String,
    default: 'Esta ação não pode ser desfeita.',
  },
});

defineEmits(['confirm', 'cancel']);
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 24px;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.modal-title {
  margin-top: 0;
  font-size: 1.25rem;
}

.modal-message {
  color: #52525b;
  margin-bottom: 24px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

button {
  padding: 8px 14px;
  border-radius: 6px;
  border: 1px solid transparent;
  font-weight: 500;
  cursor: pointer;
}

.button-secondary {
  background-color: #f4f4f5;
  border-color: #d4d4d8;
}

.button-danger {
  background-color: #dc2626;
  color: white;
}
</style>
