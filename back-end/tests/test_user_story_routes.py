import sys
import os
import pytest
import json
from typing import Any


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

DADOS_USUARIO = {
    "cpf": "123.456.789-00",
    "email": "joao.silva@teste.com",
    "nome": "Joao Silva",
    "senha": "$JoaoSilva123"
}
DADOS_PROJETO = {
    "titulo_projeto": "PROJETO 1 - Joao",
    "descricao": "Teste no banco de dados real",
    "cpf": DADOS_USUARIO['cpf']
}

DADOS_USER_STORY = {
    "titulo_user_story": "Criar relatorio de desempenho",
    "objetivo": "Avaliar o desempenho dos colaboradores",
    "beneficio": "Permitir uma avaliação justa.",
    "prioridade": "Alta"
}

@pytest.fixture
def setup_para_user_story():
    id_projeto_criado = None
    cpf_usuario =  DADOS_USUARIO["cpf"]

    try:
        try:
            usuario_rep.adicionar_usuario(**DADOS_USUARIO)
            print(f"\nAVISO SETUP: Usuário {cpf_usuario} criado.")
        except ValueError as e:
            if "já existem" not in str(e):
                raise e
            print(f"\nAVISO SETUP: Usuário {cpf_usuario} já existe.")

        id_projeto_criado = projeto_rep.adicionar_projeto(
            titulo = DADOS_PROJETO["titulo_projeto"],
            descricao = DADOS_PROJETO["descricao"],
            cpf_dono = DADOS_PROJETO["cpf"]
        )
        assert id_projeto_criado is not None, "Setup falhou ao criar projeto"
        print(f"AVISO SETUP: Projeto {id_projeto_criado} criado.")

        yield {
            "cpf": cpf_usuario,
            "id_projeto": id_projeto_criado
        }

    finally:
        print("\n--- INICIANDO LIMPEZA ---\n")
        try:
            if id_projeto_criado:
                projeto_rep.deletar_projeto(id_projeto_criado)
                print(f"Limpeza: Projeto {id_projeto_criado} deletado.")
            if cpf_usuario:
                usuario_rep.deletar_usuario(cpf_usuario)
                print(f"Limpeza: Usuário {cpf_usuario} deletado.")
        except Exception as e:
            print(f"AVISO [LIMPEZA]: Falha ao limpar fixture: {e}")

def test_criar_user_story(client, setup_para_user_story):
    id_user_story_criada = None

    try:
        id_projeto_criado = setup_para_user_story["id_projeto"]
        tabela_user_story = DADOS_USER_STORY.copy()
        tabela_user_story['id_projeto'] = id_projeto_criado

        response = client.post('/api/users-stories/', json = tabela_user_story)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. Body: {response.get_data(as_text = True)}")
        data = response.get_json()
        assert data.get('id_projeto') == id_projeto_criado
        assert data.get('titulo_user_story') == DADOS_USER_STORY['titulo_user_story']
        assert data.get('objetivo') == DADOS_USER_STORY['objetivo']
        assert data.get('beneficio') == DADOS_USER_STORY['beneficio']

        assert data.get('nivel_story') == DADOS_USER_STORY['prioridade']
        print(f"\nSUCESSO: User Story {id_user_story_criada} criada.")

    finally:
        print("\n--- INICIANDO LIMPEZA ---\n")

        if id_user_story_criada:
            try:
                user_story_rep.deletar_user_story(id_user_story_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a user story {id_user_story_criada}: {e}")

def test_deletar_user_story(client, setup_para_user_story):
    id_user_story_criada = None

    try:
        id_user_story_criada = user_story_rep.adicionar_user_story(
            id_projeto = setup_para_user_story["id_projeto"],
            **DADOS_USER_STORY
        )
        assert id_user_story_criada is not None, "Falha ao criar user story para o teste de deleção"
        response_del = client.delete(f"/api/users-stories/{id_user_story_criada}")
        assert response_del.status_code == 200, (
            f"Esperado 200 ao deletar user story, obteve {response_del.status_code}. Body: {response_del.get_data(as_text = True)}"
        )
        data_del = response_del.get_json()
        assert "mensagem" in data_del and str(id_user_story_criada) in data_del["mensagem"], "Mensagem de sucesso ausente ou incorreta"
        user_story_obj = user_story_rep.buscar_user_story_por_id(id_user_story_criada)
        if user_story_obj != []:
            assert False, f"User Story {id_user_story_criada} ainda existe no repositório ({user_story_obj}) após deleção via API"
        response_del_2 = client.delete(f"/api/users-stories/{id_user_story_criada}")
        assert response_del_2.status_code == 404, (
            f"Esperado 404 ao deletar User Story já removida, obteve {response_del_2.status_code}"
        )
        print(f"\nSUCESSO: User Story {id_user_story_criada} deletada e 404 confirmado.")
        id_user_story_criada = None

    finally:
        if id_user_story_criada:
            try:
                user_story_rep.deletar_user_story(id_user_story_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a user story {id_user_story_criada}: {e}")
