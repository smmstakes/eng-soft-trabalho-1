const projects = [
    { id: 1, name: 'Alpha' },
    { id: 2, name: 'Chacon' },
    { id: 3, name: 'Teste' },
];

export default defineEventHandler(async (event) => {
  const projectId = parseInt(event.context.params?.id || '0', 10);

  if (!projectId) {
    throw createError({ statusCode: 400, statusMessage: 'Project ID is required' });
  }

  if (event.method === 'DELETE') {
    const projectIndex = projects.findIndex(p => p.id === projectId);

    if (projectIndex === -1) {
      throw createError({ statusCode: 404, statusMessage: 'Project not found' });
    }

    // Remove o projeto da base de dados
    projects.splice(projectIndex, 1);
    console.log(`Projeto com ID ${projectId} foi deletado.`);

    return { success: true, message: `Projeto ${projectId} deletado com sucesso.` };
  }

  // Adicionar lógicas para GET, PATCH, etc
  throw createError({ statusCode: 405, statusMessage: 'Method Not Allowed' });
});
