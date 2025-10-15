<template>
    <button :class="['mode-button', mode]" @mouseover="hover = true" @mouseleave="hover = false">
        {{ text }}
    </button>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
    text: {
        type: String,
        required: true
    },
    mode: {
        type: String,
        default: 'black',
        validator: value => ['black', 'white'].includes(value)
    }
})

const hover = ref(false)
</script>

<style scoped>
.mode-button {
    font-weight: 400;
    height: 40px;
    padding: 0px 30px;
    border: none;
    border-radius: 6px;
    transition: 0.5s;
    cursor: pointer;
}

.mode-button.black {
    background-color: #171717;
    color: white;
}

.mode-button.black:hover {
    background-color: #fff;
    color: black;
    border: 1px solid #D4D4D4;
}

.mode-button.white {
    background-color: #fff;
    color: black;
    border: 1px solid #D4D4D4;
}

.mode-button.white:hover {
    background-color: #171717;
    color: white;
    border: none;
}
</style>