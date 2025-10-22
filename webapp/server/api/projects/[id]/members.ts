interface Member {
  id: number;
  name: string;
  email: string;
  avatarUrl: string;
  role: 'Product Owner' | 'Scrum Master' | 'Desenvolvedor';
  isCurrentUser?: boolean; // Para identificar o usuário logado
}

// Mock de dados 
const membersByProject: Record<string, Member[]> = {
  '1': [
    { id: 101, name: 'Maria Silva', email: 'maria@empresa.com', avatarUrl: 'https://i.pravatar.cc/40?u=maria', role: 'Product Owner', isCurrentUser: true },
    { id: 102, name: 'João Santos', email: 'joao@empresa.com', avatarUrl: 'https://i.pravatar.cc/40?u=carlos', role: 'Scrum Master' },
    { id: 103, name: 'Ana Costa', email: 'ana@empresa.com', avatarUrl: 'https://i.pravatar.cc/40?u=ana', role: 'Desenvolvedor' },
  ],

  '2': [
    { id: 101, name: 'Maria Silva', email: 'maria@empresa.com', avatarUrl: 'https://i.pravatar.cc/40?u=maria', role: 'Product Owner', isCurrentUser: true },
    { id: 202, name: 'Carlos Pereira', email: 'carlos@empresa.com', avatarUrl: 'https://i.pravatar.cc/40?u=carlos', role: 'Desenvolvedor' },
  ],

  'default': [
    { id: 101, name: 'Maria Silva', email: 'maria@empresa.com', avatarUrl: 'https://i.pravatar.cc/40?u=maria', role: 'Product Owner', isCurrentUser: true },
  ]
};


export default defineEventHandler((event) => {
  const projectId = event.context.params?.id;

  if (!projectId) {
    throw createError({ statusCode: 400, statusMessage: 'Necessário fornecer o ID do projeto' });
  }

  // Retorna os membros para o projeto específico ou um default
  return membersByProject[projectId] || membersByProject['default'];
});
