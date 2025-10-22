<template>
  <div class="members-card">
    <h2>Gerenciamento de Membros</h2>

    <div v-if="members.length > 0" class="members-list">
      <div v-for="member in sortedMembers" :key="member.id" class="member-item">
        
        <div class="member-info">
          <img :src="member.avatarUrl" alt="Avatar" class="avatar">

          <div>
            <span class="member-name">
              {{ member.name }}
              <span v-if="member.isCurrentUser" class="you-tag">(Você)</span>
            </span>
            <span class="member-email">{{ member.email }}</span>
          </div>

        </div>

        <div class="member-role">

          <span v-if="member.role === 'Product Owner'">Product Owner</span>
          <select v-else v-model="member.role" @change="onRoleChange(member, $event)">
            <option>Scrum Master</option>
            <option>Desenvolvedor</option>
          </select>

        </div>
      </div>
    </div>

    <div v-else>
      Carregando membros...
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Member, Role } from '../../composables/states';

const members = useProjectMembers();
const toasts = useToasts();

const sortedMembers = computed(() => {
  return [...members.value].sort((a, b) => {
    if (a.role === 'Product Owner') return -1;
    if (b.role === 'Product Owner') return 1;
    return 0;
  });
});

const onRoleChange = (member: Member, event: Event) => {
  const newRole = (event.target as HTMLSelectElement).value as Role;
  toasts.info(`Mudando o papel de ${member.name} (ID: ${member.id}) para ${newRole}`);
  
  // AQUI você faria a chamada de API para salvar a alteração no backend
  // Exemplo:
  // await $fetch(`/api/members/${member.id}/role`, {
  //   method: 'PATCH',
  //   body: { role: newRole }
  // });
  
  // O v-model atualiza a UI, mas a chamada persistiria a mudança.
};
</script>

<style scoped>
.members-card {
  background-color: #ffffff;
  border: 1px solid #E5E5E5;
  border-radius: 8px;
  padding: 24px;
  max-width: 964px;
}

h2 {
  font-size: large;
  font-weight: 400;
  color: #171717;
  margin-top: 0;
  margin-bottom: 24px;
}

.member-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.member-item + .member-item {
  margin-top: 12px;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.member-info div {
  display: flex;
  flex-direction: column;
}

.member-name {
  font-weight: 500;
  color: #171717;
}

.you-tag {
  color: #71717a;
  font-weight: 400;
}

.member-email {
  color: #71717a;
  font-size: 0.875rem;
}

.member-role select {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #d4d4d8;
  background-color: #fff;
  font-size: 0.875rem;
}

.member-role span {
  font-size: 0.875rem;
  font-weight: 500;
  color: #3f3f46;
  padding: 6px 10px;
}
</style>
