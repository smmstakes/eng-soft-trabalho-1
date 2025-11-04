<template>
  <div class="main-wrapper">

    <Header title="Configurações do Projeto" description="Gerencie configurações essenciais e membros do projeto">
    </Header>

    <div class="main-content">
      <div class="mt-8">
        <ProjectSettingsCard />
      </div>

      <div class="mt-8">
        <ProjectMembersCard />
      </div>

      <div class="mt-8">
        <ProjectPasswordCard />
      </div>

      <div class="mt-8">
        <DangerZoneCard />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProject } from '@/composables/useProject'
const project = useProject()

definePageMeta({
  layout: 'config'
});

</script>

<style scoped>
.mt-8 {
  margin-top: 24px;
}

.main-content {
  padding: 20px 32px;
}

</style>
