<template>
  <div class="main-wrapper">
		
    <div class="page-content" v-if="project">
      <h1 class="config-title">Configurações do Projeto - {{ project.name }}</h1>
      <h3 class="config-description">Gerencie configurações essenciais e membros do projeto</h3>
    </div>

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
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'config'
});

const project = useProject();
</script>

<style scoped>
.config-title {
	color: #171717;
  font-size: x-large;
	font-weight: 500;
  margin: 4px;
  padding-bottom: 4px;
}

.config-description {
  color: #171717;
  font-size: medium;
  font-weight: 400;
	margin: 4px;
  padding-top: 4px;
}

.mt-8 {
 margin-top: 24px;
}
</style>
