<template>
  <div class="card" @click="goToProject">
    <div class="icon-container">
      <component :is="icon" class="icon" />
    </div>
    <div class="card-body">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-description">{{ description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProject } from '@/composables/useProject'
import { useRouter } from 'vue-router'
import * as icons from 'lucide-vue-next'

const props = defineProps<{
  id?: number
  projectId: string
  title: string
  description: string
  icon?: string
}>()

const router = useRouter()
const projectState = useProject()
const icon = icons[props.icon || 'FolderKanban'] || icons.FolderKanban

const goToProject = () => {
  projectState.value = {
    id: props.id || 0,
    projectId: props.projectId,
    name: props.title,
    description: props.description,
    sprintStatus: ''
  }
  router.push('/configuration')
}
</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  border: 1px solid #d4d4d4;
  border-radius: 6px;
  padding: 14px;
  width: 220px;
  background-color: #fff;
  cursor: pointer;
  transition: box-shadow 0.2s ease, transform 0.1s ease;
}
.card:hover {
  box-shadow: 0 3px 8px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}
.icon-container {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  background-color: #E5E5E5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}
.icon {
  color: white;
  width: 28px;
  height: 28px;
}
.card-title {
  font-weight: 600;
  font-size: 1rem;
  color: #171717;
  margin: 0 0 4px 0;
}
.card-description {
  font-size: 0.9rem;
  color: #525252;
  margin: 0;
}
</style>
