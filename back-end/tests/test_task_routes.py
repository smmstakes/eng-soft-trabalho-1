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
from app.models import task_rep, sprint_rep, usuario_rep, projeto_rep

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
    "senha": "$JoaoSilva123"
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
DADOS_TASK = {
    "nome_estado": "A Fazer",
    "descricao_task": "Terminar a rota Task",
    "nivel_task": "Alta"
}
DADOS_TASK_2 = {
    "nome_estado": "A Fazer",
    "descricao_task": "Terminar a rota o Backend",
    "nivel_task": "Alta"
}
DADOS_TASK_3 = {
    "nome_estado": "A Fazer",
    "descricao_task": "Se formar na UnB",
    "nivel_task": "Alta"
}

@pytest.fixture
def setup_para_task(client):
    id_projeto_criado = None
    id_sprint_criada = None
    cpf_usuario = DADOS_USUARIO["cpf"]
    token_de_acesso = None

    try:
        try:
            usuario_rep.adicionar_usuario(**DADOS_USUARIO)
            print(f"\nAVISO SETUP: Usuário {cpf_usuario} criado.")
        except ValueError as e:
            if "já existem" not in str(e) and "UNIQUE constraint failed" not in str(e):
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

        id_sprint_criada = sprint_rep.adicionar_sprint(
            id_projeto = id_projeto_criado,
            **DADOS_SPRINT
        )
        assert id_sprint_criada is not None, "Setup falhou ao criar sprint"
        print(f"AVISO SETUP: Sprint {id_sprint_criada} criada.")

        yield {
            "cpf": cpf_usuario,
            "id_projeto": id_projeto_criado,
            "id_sprint": id_sprint_criada,
            "token": token_de_acesso
            }
    finally:
        print("\n--- INICIANDO LIMPEZA (Fixture Task) ---\n")
        try:
            if id_sprint_criada:
                sprint_rep.deletar_sprint(id_sprint_criada)
                print(f"Limpeza: Sprint {id_sprint_criada} deletada.")
            if id_projeto_criado:
                projeto_rep.deletar_projeto(id_projeto_criado)
                print(f"Limpeza: Projeto {id_projeto_criado} deletado.")
            if cpf_usuario:
                usuario_rep.deletar_usuario(cpf_usuario)
                print(f"Limpeza: Usuário {cpf_usuario} deletado.")
        except Exception as e:
            print(f"AVISO [LIMPEZA]: Falha ao limpar fixture: {e}")

def test_criar_task(client, setup_para_task):
    id_task_criada = None
    id_sprint_criada = setup_para_task["id_sprint"]

    try:
        tabela_task = DADOS_TASK.copy()
        tabela_task['id_sprint'] = id_sprint_criada

        token_de_acesso = setup_para_task["token"]
        headers = {'Authorization': f'Bearer {token_de_acesso}'}
        response = client.post('/api/tasks/', json = tabela_task, headers = headers)

        assert response.status_code == 201, (
            f"Esperado 201, obteve {response.status_code}. Body: {response.get_data(as_text = True)}"
        )
        data = response.get_json()

        id_task_criada = data.get('id_task')
        assert id_task_criada is not None
        assert data.get('cpf') == setup_para_task["cpf"]
        assert data.get('id_sprint') == setup_para_task["id_sprint"]
        print(f"\nSUCESSO: Task {id_task_criada} criada para o usuário correto.")

    finally:
        if id_task_criada:
            try:
                task_rep.deletar_task(id_task_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a task {id_task_criada}: {e}")

def test_deletar_tasks(client, setup_para_task):
    id_task_criada = None
    try:
        id_sprint_criada = setup_para_task["id_sprint"]
        cpf_do_usuario = setup_para_task["cpf"]
        token = setup_para_task["token"]
        headers = {'Authorization': f'Bearer {token}'}

        id_task_criada = task_rep.adicionar_task(id_sprint = id_sprint_criada,
                                                   cpf = cpf_do_usuario,
                                                   ** DADOS_TASK)

        assert id_task_criada is not None, "Falha no setup do teste de deleção"
        response_del = client.delete(f"/api/tasks/{id_task_criada}", headers = headers)

        assert response_del.status_code == 200, (
            f"Esperado 200 ao deletar task, obteve {response_del.status_code}. Body: {response_del.get_data(as_text = True)}"
        )
        data_del = response_del.get_json()
        assert "mensagem" in data_del
        assert str(id_task_criada) in data_del["mensagem"], "Mensagem de sucesso ausente ou incorreta"
        tasks_obj = task_rep.listar_task(id_task = id_task_criada)
        if tasks_obj != []:
            assert False, f"Task {id_task_criada} ainda existe no repositório ({tasks_obj}) após deleção via API"
        response_del_2 = client.delete(f"/api/tasks/{id_task_criada}", headers = headers)
        assert response_del_2.status_code == 404, (
            f"Esperado 404 ao deletar task já removida, obteve {response_del_2.status_code}"
        )
        id_task_criada = None

    finally:
        if id_task_criada:
            try:
                task_rep.deletar_task(id_task_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a task {id_task_criada}: {e}")


def test_listar_tasks(client, setup_para_task):
    id_sprint_criada_1 = None
    id_sprint_criada_2 = None
    id_task_criada_1 = None
    id_task_criada_2 = None
    id_task_criada_3 = None

    try:
        id_sprint_criada_1 = setup_para_task["id_sprint"]
        cpf_usuario = setup_para_task["cpf"]
        id_projeto_criado = setup_para_task["id_projeto"]
        token = setup_para_task["token"]

        headers = {'Authorization': f'Bearer {token}'}

        id_task_criada_1 = task_rep.adicionar_task(id_sprint = id_sprint_criada_1,
                                                   cpf = cpf_usuario,
                                                   ** DADOS_TASK)

        id_task_criada_2 = task_rep.adicionar_task(id_sprint = id_sprint_criada_1,
                                                   cpf = cpf_usuario,
                                                   **DADOS_TASK_2)

        id_sprint_criada_2 = sprint_rep.adicionar_sprint(id_projeto = id_projeto_criado,
                                                         ** DADOS_SPRINT_2)

        id_task_criada_3 = task_rep.adicionar_task(id_sprint = id_sprint_criada_2,
                                                   cpf = cpf_usuario,
                                                   **DADOS_TASK_3)

        assert all([id_task_criada_1, id_task_criada_2, id_task_criada_3, id_sprint_criada_2]), "Falha no setup do teste de listagem"

        response_por_cpf = client.get('/api/tasks/', headers = headers)
        assert response_por_cpf.status_code == 200
        data_por_cpf = response_por_cpf.get_json()
        assert isinstance(data_por_cpf, list) and len(data_por_cpf) == 3, f"Esperado 3 tasks, API retornou {len(data_por_cpf)}"

        response_por_sprint_1 = client.get(f'/api/tasks/?id_sprint={id_sprint_criada_1}', headers = headers)
        assert response_por_sprint_1.status_code == 200
        data_por_sprint_1 = response_por_sprint_1.get_json()
        assert isinstance(data_por_sprint_1, list) and len(data_por_sprint_1) == 2, f"Esperado 2 tasks ao filtrar pela Sprint 1, API retornou {len(data_por_sprint_1)}"

        response_por_sprint_2 = client.get(f'/api/tasks/?id_sprint={id_sprint_criada_2}', headers = headers)
        assert response_por_sprint_2.status_code == 200
        data_por_sprint_2 = response_por_sprint_2.get_json()
        assert isinstance(data_por_sprint_2, list) and len(data_por_sprint_2) == 1, f"Esperado 1 task ao filtrar pela Sprint 2, API retornou {len(data_por_sprint_2)}"

    finally:
        try:
            if id_task_criada_1: task_rep.deletar_task(id_task_criada_1)
            if id_task_criada_2: task_rep.deletar_task(id_task_criada_2)
            if id_task_criada_3: task_rep.deletar_task(id_task_criada_3)
            if id_sprint_criada_2: sprint_rep.deletar_sprint(id_sprint_criada_2)
        except Exception as e:
            print(f"AVISO: Falha ao limpar tasks/sprint 2 de listagem: {e}")

