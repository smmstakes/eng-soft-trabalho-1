import sys
import os
import pytest
import json
from typing import Any
from flask_jwt_extended import create_access_token

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
    "cpf": "133.446.789-00",
    "email": "felipeduarte@gmail.com",
    "nome": "Felipe Duarte",
    "senha": "$FelipeDuarte123"
}
DADOS_PROJETO = {
    "titulo_projeto": "PROJETO 1 - Joao",
    "descricao": "Teste no banco de dados real",
    "cpf": DADOS_USUARIO['cpf'],
    "senha": "$JoaoSilva123"
}

DADOS_USER_STORY = {
    "titulo_user_story": "Criar relatorio",
    "objetivo": "Avaliar o desempenho dos participantes",
    "beneficio": "Permitir uma avaliação justa.",
    "prioridade": "Alta"
}
DADOS_USER_STORY_2 = {
    "titulo_user_story": "Terminar o trabalho de ES",
    "objetivo": "Terminar os documentos e código",
    "beneficio": "Passar em ES",
    "prioridade": "Alta"
}

@pytest.fixture
def setup_para_user_story(client):
    id_projeto_criado = None
    cpf_usuario =  DADOS_USUARIO["cpf"]
    token_de_acesso = None

    try:
        try:
            usuario_rep.adicionar_usuario(**DADOS_USUARIO)
            print(f"\nAVISO SETUP: Usuário {cpf_usuario} criado.")
        except ValueError as e:
            if "já existem" not in str(e):
                raise e
            print(f"\nAVISO SETUP: Usuário {cpf_usuario} já existe.")

        with client.application.app_context():
            token_de_acesso = create_access_token(identity = cpf_usuario)

        id_projeto_criado = projeto_rep.adicionar_projeto(
            titulo = DADOS_PROJETO["titulo_projeto"],
            descricao = DADOS_PROJETO["descricao"],
            senha = DADOS_PROJETO["senha"],
            cpf_dono = DADOS_PROJETO["cpf"]
        )
        assert id_projeto_criado is not None, "Setup falhou ao criar projeto"
        print(f"AVISO SETUP: Projeto {id_projeto_criado} criado.")

        yield {
            "cpf": cpf_usuario,
            "id_projeto": id_projeto_criado,
            "token": token_de_acesso
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

        cpf_usuario = setup_para_user_story["cpf"]
        with client.application.app_context():
            token_de_acesso = create_access_token(identity = cpf_usuario)
        headers = {'Authorization': f'Bearer {token_de_acesso}'}
        response = client.post('/api/users-stories/', json = tabela_user_story, headers = headers)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. Body: {response.get_data(as_text = True)}")
        data = response.get_json()
        id_user_story_criada = data.get('id_user_story')
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
        headers = {'Authorization': f'Bearer {setup_para_user_story["token"]}'}
        response_del = client.delete(f"/api/users-stories/{id_user_story_criada}", headers = headers)
        assert response_del.status_code == 200, (
            f"Esperado 200 ao deletar user story, obteve {response_del.status_code}. Body: {response_del.get_data(as_text = True)}"
        )
        data_del = response_del.get_json()
        assert "mensagem" in data_del and str(id_user_story_criada) in data_del["mensagem"], "Mensagem de sucesso ausente ou incorreta"
        user_story_obj = user_story_rep.buscar_user_story_por_id(id_user_story_criada)
        if user_story_obj != []:
            assert False, f"User Story {id_user_story_criada} ainda existe no repositório ({user_story_obj}) após deleção via API"
        response_del_2 = client.delete(f"/api/users-stories/{id_user_story_criada}", headers = headers)
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

def test_listar_users_stories_do_projeto(client, setup_para_user_story):
    id_user_story_criada_1 = None
    id_user_story_criada_2 = None
    id_projeto_criado = setup_para_user_story["id_projeto"]

    try:
        id_user_story_criada_1 = user_story_rep.adicionar_user_story(
            id_projeto = id_projeto_criado,
            **DADOS_USER_STORY
        )
        id_user_story_criada_2 = user_story_rep.adicionar_user_story(
            id_projeto = id_projeto_criado,
            **DADOS_USER_STORY_2
        )
        assert id_user_story_criada_1 and id_user_story_criada_2, "Falha ao criar User Stories para o teste de listagem"

        cpf_usuario = setup_para_user_story["cpf"]
        with client.application.app_context():
            token_de_acesso = create_access_token(identity = cpf_usuario)
        headers = {'Authorization': f'Bearer {token_de_acesso}'}
        response = client.get(f'/api/users-stories/por-projeto/{id_projeto_criado}', headers = headers)

        assert response.status_code == 200, (
             f"Esperado 200, obteve {response.status_code}. Body: {response.get_data(as_text = True)}"
        )
        data = response.get_json()
        assert isinstance(data, list), "API não retornou uma lista (array)"
        assert len(data) == 2, f"Esperado 2 User Stories, mas a API retornou {len(data)}"
        titulos_retornados = {user_story['titulo_user_story'] for user_story in data}
        assert titulos_retornados == {DADOS_USER_STORY["titulo_user_story"], DADOS_USER_STORY_2["titulo_user_story"]}, "Os dados das User Stories retornadas estão incorretos"
        print(f"\nSUCESSO: API listou 2 User Stories para o projeto {id_projeto_criado}.\n")

    finally:
        try:
            if id_user_story_criada_1:
                user_story_rep.deletar_user_story(id_user_story_criada_1)
            if id_user_story_criada_2:
                user_story_rep.deletar_user_story(id_user_story_criada_2)
        except Exception as e:
            print(f"AVISO: Falha ao limpar User Stories de listagem: {e}")