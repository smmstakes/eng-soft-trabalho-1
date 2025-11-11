<template>
    <div class="main-wrapper">
        <Header title="Sprints" description="Gerencie e acompanhe o progresso das suas sprints">
            <Button @click="showCreateModal = true" text="+ Criar Nova Sprint" mode="black" />
        </Header>

        <!-- <div class="main-content">
            <div class="mt-8" v-if="sprints.value.length > 0">
                <SprintCard v-for="sprint in sprints.value" :key="sprint.id" :sprint="sprint" />
            </div>

            <div class="mt-8" v-else>
                <p>Ainda não há sprints cadastradas para este projeto.</p>
            </div>
        </div> -->


        <Modal title="Criar Sprint" v-model:show="showCreateModal">
            <form @submit.prevent="submitCreateSprint">
                <div class="form-group">
                    <label>Título *</label>
                    <input v-model="form.meta" type="text" placeholder="Digite o título" required />
                </div>

                <div class="form-group">
                    <label>Meta *</label>
                    <textarea v-model="form.inicio" placeholder="Digite a data de início" required />
                </div>

                <div class="form-group">
                    <label>Término *</label>
                    <textarea v-model="form.termino" placeholder="Digite a data de término" required />
                </div>

                <div class="form-group">
                    <label>Revisão da Sprint</label>
                    <textarea v-model="form.revisao_sprint" placeholder="Digite a revisão" />
                </div>

                <Button text="Criar" mode="black" type="submit" />
            </form>
        </Modal>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useProject, useProjectSprints } from '@/composables/useProject';
import { criarSprint } from '@/server/services/projectService';
import { useAuth } from '@/composables/useAuth';

definePageMeta({ layout: 'config' })

const project = useProject();
const sprints = useProjectSprints();
const auth = useAuth();

const showCreateModal = ref(false);

const form = ref({
    meta: '',
    inicio: '',
    termino: '',
    revisao_sprint: ''
});

const submitCreateSprint = async () => {
    if (!project.value) return;

    try {
        const novaSprint = await criarSprint(project.value.id, form.value, auth.value.token!);
        sprints.value.push(novaSprint);

        showCreateModal.value = false;
        form.value = { meta: '', inicio: '', termino: '', revisao_sprint: '' };
    } catch (err: any) {
        console.error(err);
        alert(err.message || 'Erro ao criar sprint');
    }
};
</script>

<style scoped>
.mt-8 {
    margin-top: 24px;
}

.main-content {
    padding: 20px 32px;
}

.main-content p {
    font-size: 1rem;
    color: #6b7280;
}
</style>
