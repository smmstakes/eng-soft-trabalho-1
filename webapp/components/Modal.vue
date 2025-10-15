<template>
    <transition name="fade">
        <div v-if="show" class="modal-overlay" @click.self="close">
            <div class="modal-content">
                <!-- Botão de fechar -->
                <button class="close-btn" @click="close">×</button>
                <slot></slot>
            </div>
        </div>
    </transition>
</template>

<script setup>
const props = defineProps({
    show: Boolean
})
const emit = defineEmits(['update:show'])

function close() {
    emit('update:show', false)
}
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
}

.modal-content {
    position: relative;
    /* necessário para posicionar o botão de fechar */
    background-color: white;
    width: 600px;
    max-width: 90%;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
    max-height: 80vh;
    overflow-y: auto;
}

/* Botão X no canto superior direito */
.close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: transparent;
    border: none;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
    line-height: 1;
}

.close-btn:hover {
    color: #D4D4D4;
}

/* animação de entrada/saída */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>