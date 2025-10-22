const projects = [
    { id: 1, name: 'Alpha' },
    { id: 2, name: 'Chacon' },
    { id: 3, name: 'Teste' },
];

export default defineEventHandler(async (event) => {
  const projectId = parseInt(event.context.params?.id || '0', 10);

  if (!projectId) {
    throw createError({ statusCode: 400, statusMessage: 'Necessário fornecer o ID do projeto' });
  }

  if (event.method === 'DELETE') {
    const projectIndex = projects.findIndex(p => p.id === projectId);

    if (projectIndex === -1) {
      throw createError({ statusCode: 404, statusMessage: 'Projeto não encontrado' });
    }

    // Remove o projeto da base de dados
    projects.splice(projectIndex, 1);

    return { success: true, message: `Projeto ${projectId} deletado com sucesso.` };
  }

  // Adicionar lógicas para GET, PATCH, etc
  throw createError({ statusCode: 405, statusMessage: 'Método não permitido' });
});
