<template>
  <Modal :title="title" v-model:show="internalShow">
    
    <div class="confirm-content">
      <p>{{ message }}</p>
    </div>

    <div class="confirm-actions">
      <Button 
        text="Cancelar" 
        mode="secondary" @click="onCancel"
      />
      <Button 
        :text="confirmText" 
        mode="danger" 
        @click="onConfirm"
      />
    </div>

  </Modal>
</template>

<script setup lang="ts">
import { computed } from 'vue';
// Assumindo que Modal e Button são componentes globais ou importados
// import Modal from '~/components/global/Modal.vue';
// import Button from '~/components/global/Button.vue';

const props = withDefaults(defineProps<{
  show: boolean,
  title: string,
  message: string,
  confirmText?: string
}>(), {
  confirmText: 'Confirmar' // Texto padrão para o botão
});

const emit = defineEmits(['update:show', 'confirm', 'cancel']);

// 2. Sincroniza o v-model (prop 'show')
const internalShow = computed({
  get: () => props.show,
  set: (val) => emit('update:show', val)
});

// 3. Emite o evento 'confirm' e fecha o modal
const onConfirm = () => {
  emit('confirm');
  internalShow.value = false;
};

// 4. Emite o evento 'cancel' (opcional) e fecha o modal
const onCancel = () => {
  emit('cancel');
  internalShow.value = false;
};
</script>

<style scoped>
.confirm-content p {
  font-size: 1rem;
  color: #374151; /* Cinza escuro */
  line-height: 1.5;
  margin-bottom: 16px;
}
.confirm-actions {
  display: flex;
  justify-content: flex-end; /* Alinha botões à direita */
  gap: 12px;
  margin-top: 24px;
}
</style>