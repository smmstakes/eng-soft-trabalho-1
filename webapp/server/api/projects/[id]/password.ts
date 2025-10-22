// Mock de senhas (em um app real, viria de um banco de dados e seria criptografado)
const passwordsByProject: Record<string, string> = {
  '1': 'alpha123',
  '2': 'chacon_secure',
  '3': 'teste_pass',
};

export default defineEventHandler(async (event) => {
  const projectId = event.context.params?.id;

  if (!projectId) {
    throw createError({ statusCode: 400, statusMessage: 'Necessário fornecer o ID do projeto' });
  }


  // Se a requisição for do tipo PATCH (atualização)
  if (event.method === 'PATCH') {
    const body = await readBody(event);
    if (!body.password || body.password.length < 8 || !/[A-Za-z]/.test(body.password) ||
      !/[0-9]/.test(body.password)) {
      throw createError({ statusCode: 400, statusMessage: 'A senha deve ter pelo menos 8 caracteres e conter letras e números' });
    }


      passwordsByProject[projectId] = body.password;

    return { success: true, message: 'Senha atualizada com sucesso!' };
  }
  

  if (event.method === 'GET') {
    return { password: passwordsByProject[projectId] || '' };
  }

  // Rejeita outros métodos HTTP
  throw createError({ statusCode: 405, statusMessage: 'Método não permitido' });
});
