import sys
import os
import pytest
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from run import create_app
from app.models import usuario_rep, projeto_rep, user_story_rep

@pytest.fixture
def client():
    app_instance = create_app()
    with app_instance.test_client() as client:
        yield client

DADOS_USUARIO_DONO = {
    "cpf": "123.456.789-00",
    "email": "joao.silva@teste.com",
    "nome": "Joao Silva",
    "senha": "$JoaoSilva123"
}
DADOS_PROJETO_TESTE = {
    "titulo_projeto": "PROJETO 1 - Joao",
    "descricao": "Teste no banco de dados real",
    "cpf": DADOS_USUARIO_DONO['cpf']
}

DADOS_USER_STORY_TESTE = {
    "titulo_user_story": "Criar relatorio de desempenho",
    "objetivo": "Avaliar o desempenho dos colaboradores",
    "beneficio": "Permitir uma avaliação justa.",
    "prioridade": "Alta"
}

def test_criar_e_limpar_user_story(client):

    id_user_story_criada = None
    id_projeto_criado = None
    cpf_usuario = DADOS_USUARIO_DONO['cpf']

    try:
        try:
            usuario_rep.adicionar_usuario(
                    cpf = DADOS_USUARIO_DONO["cpf"],
                    email = DADOS_USUARIO_DONO["email"],
                    nome = DADOS_USUARIO_DONO["nome"],
                    senha = DADOS_USUARIO_DONO["senha"]
                )

        except ValueError as e:
            if "já existem" in str(e):
                print(f"AVISO SETUP: Usuário {DADOS_USUARIO_DONO['cpf']} já existe.")
            else:
                assert False, f"Falha no SETUP (adicionar_usuario): {e}"

        try:
            id_projeto_criado = projeto_rep.adicionar_projeto(
                titulo = DADOS_PROJETO_TESTE["titulo_projeto"],
                descricao = DADOS_PROJETO_TESTE["descricao"],
                cpf_dono = DADOS_PROJETO_TESTE["cpf"]
            )

            assert id_projeto_criado is not None, "Falha ao obter id_projeto do setup"
            print(f"AVISO SETUP: Projeto {id_projeto_criado} criado.")

        except Exception as e:
            assert False, f"Falha no SETUP (adicionar_projeto): {e}"

        tabela_user_story = DADOS_USER_STORY_TESTE.copy()
        tabela_user_story['id_projeto'] = id_projeto_criado

        response = client.post('/api/users-stories/', json = tabela_user_story)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. Body: {response.get_data(as_text=True)}")
        data = response.get_json()

        id_user_story_criada = data.get('id_user_story')
        assert data.get('id_projeto') == id_projeto_criado
        assert data.get('titulo_user_story') == DADOS_USER_STORY_TESTE['titulo_user_story']
        assert data.get('objetivo') == DADOS_USER_STORY_TESTE['objetivo']
        assert data.get('beneficio') == DADOS_USER_STORY_TESTE['beneficio']
        assert data.get('nivel_story') == DADOS_USER_STORY_TESTE['prioridade']
        print(f"\nSUCESSO: User Story {id_user_story_criada} criada.")

    finally:
        print("\n--- INICIANDO LIMPEZA ---\n")

        if id_user_story_criada:
            try:
                user_story_rep.deletar_user_story(id_user_story_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a user story {id_user_story_criada}: {e}")

        if id_projeto_criado:
            try:
                projeto_rep.deletar_projeto(id_projeto_criado)
            except Exception as e:
                print(f"AVISO: Falha ao limpar o projeto {id_projeto_criado}: {e}")

        if cpf_usuario:
            try:
                usuario_rep.deletar_usuario(cpf_usuario)
            except Exception as e:
                print(f"AVISO: Falha ao limpar o usuário {cpf_usuario}: {e}")
