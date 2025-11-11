<template>
  <div class="main-wrapper">
    <Header title="Configurações do Projeto" description="Gerencie o projeto" />

    <div class="main-content">
      <ProjectSettingsCard />
      <ProjectMembersCard />
      <ProjectPasswordCard />
      <DangerZoneCard />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProject } from '@/composables/useProject'
const project = useProject()

definePageMeta({ layout: 'config' })
</script>

