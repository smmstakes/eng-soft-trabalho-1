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
from app.models import usuario_rep, projeto_rep, sprint_rep

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
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
    "senha": "A123"
}
DADOS_SPRINT = {
    "meta": "Entregar o MVP",
    "inicio": "2025-11-10",
    "termino": "2025-11-20",
    "revisao_sprint": "Revisao ao final do periodo.",
}
DADOS_SPRINT_2 = {
    "meta": "Terminar o trabalho de ES",
    "inicio": "2025-11-15",
    "termino": "2025-11-25",
    "revisao_sprint": "Revisar o código e docs",
}

@pytest.fixture
def setup_para_sprint(client):
    id_projeto_criado = None
    cpf_usuario = DADOS_USUARIO["cpf"]
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


def test_criar_sprint(client, setup_para_sprint):
    id_sprint_criada = None
    id_projeto_criado = setup_para_sprint["id_projeto"]

    try:
        tabela_sprint = DADOS_SPRINT.copy()
        tabela_sprint['id_projeto'] = id_projeto_criado

        cpf_usuario = setup_para_sprint["cpf"]
        with client.application.app_context():
            token_de_acesso = create_access_token(identity = cpf_usuario)
        headers = {'Authorization': f'Bearer {token_de_acesso}'}
        response = client.post('/api/sprints/', json = tabela_sprint, headers = headers)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. Body: {response.get_data(as_text = True)}"
        )
        data = response.get_json()
        id_sprint_criada = data.get('id_sprint')
        assert data.get('id_projeto') == id_projeto_criado
        assert data.get('meta') == DADOS_SPRINT['meta']
        assert data.get('inicio') == DADOS_SPRINT['inicio']
        assert data.get('termino') == DADOS_SPRINT['termino']

    finally:
        if id_sprint_criada:
            try:
                sprint_rep.deletar_sprint(id_sprint_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a sprint {id_sprint_criada}: {e}")

def test_deletar_sprint(client, setup_para_sprint):
    id_sprint_criada = None

    try:
        id_sprint_criada = sprint_rep.adicionar_sprint(
            id_projeto = setup_para_sprint["id_projeto"],
            **DADOS_SPRINT
        )
        assert id_sprint_criada is not None, "Falha ao criar sprint para o teste de deleção"
        headers = {'Authorization': f'Bearer {setup_para_sprint["token"]}'}
        response_del = client.delete(f"/api/sprints/{id_sprint_criada}", headers = headers)
        assert response_del.status_code == 200, (
            f"Esperado 200 ao deletar sprint, obteve {response_del.status_code}. Body: {response_del.get_data(as_text = True)}"
        )
        data_del = response_del.get_json()
        assert "mensagem" in data_del and str(id_sprint_criada) in data_del["mensagem"], "Mensagem de sucesso ausente ou incorreta"
        sprint_obj = sprint_rep.buscar_sprint_por_id(id_sprint_criada)
        if sprint_obj is not None:
            assert False, f"Sprint {id_sprint_criada} ainda existe no repositório ({sprint_obj}) após deleção via API"
        response_del_2 = client.delete(f"/api/sprints/{id_sprint_criada}", headers = headers)
        assert response_del_2.status_code == 404, (
            f"Esperado 404 ao deletar sprint já removida, obteve {response_del_2.status_code}"
        )
        print(f"\nSUCESSO: Sprint {id_sprint_criada} deletada e 404 confirmado.")
        id_sprint_criada = None

    finally:
        if id_sprint_criada:
            try:
                sprint_rep.deletar_sprint(id_sprint_criada)
                print(f"AVISO (Safety Net): Sprint {id_sprint_criada} deletada.")
            except Exception as e:
                print(f"AVISO: Falha ao limpar a sprint {id_sprint_criada}: {e}")

def test_listar_sprints_do_projeto(client, setup_para_sprint):
    id_sprint_criada_1 = None
    id_sprint_criada_2 = None
    id_projeto_criado = setup_para_sprint["id_projeto"]

    try:
        id_sprint_criada_1 = sprint_rep.adicionar_sprint(
            id_projeto = id_projeto_criado,
            **DADOS_SPRINT
        )
        id_sprint_criada_2 = sprint_rep.adicionar_sprint(
            id_projeto = id_projeto_criado,
            **DADOS_SPRINT_2
        )
        assert id_sprint_criada_1 and id_sprint_criada_2, "Falha ao criar sprints para o teste de listagem"

        cpf_usuario = setup_para_sprint["cpf"]
        with client.application.app_context():
            token_de_acesso = create_access_token(identity = cpf_usuario)
        headers = {'Authorization': f'Bearer {token_de_acesso}'}
        response = client.get(f"/api/sprints/por-projeto/{id_projeto_criado}", headers = headers)

        assert response.status_code == 200, (
             f"Esperado 200, obteve {response.status_code}. Body: {response.get_data(as_text = True)}"
        )
        data = response.get_json()
        assert isinstance(data, list), "API não retornou uma lista (array)"
        assert len(data) == 2, f"Esperado 2 sprints, mas a API retornou {len(data)}"

        assert isinstance(data[0]['inicio'], str), "As datas não foram convertida para string corretamente"
        print(f"\nSUCESSO: API listou 2 sprints para o projeto {id_projeto_criado}.")

    finally:
        try:
            if id_sprint_criada_1:
                sprint_rep.deletar_sprint(id_sprint_criada_1)
            if id_sprint_criada_2:
                sprint_rep.deletar_sprint(id_sprint_criada_2)
        except Exception as e:
            print(f"AVISO: Falha ao limpar sprints de listagem: {e}")