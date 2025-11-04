import sys
import os
import pytest
import json
from typing import Any

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
DADOS_SPRINT = {
    "meta": "sim",
    "inicio": "2001-12-13",
    "termino": "2001-12-31",
    "revisao_sprint": "sim",
}
DADOS_TASK: dict[str, Any] = {
    "nome_estado": "Concluido",
    "descricao_task": "sim",
    "nivel_task": "Baixa"
}

def test_criar_task_e_limpar(client):
    id_task_criado = None
    id_sprint_criada = None
    id_projeto_criado = None
    cpf_usuario = DADOS_USUARIO_DONO["cpf"]

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
                print(f"AVISO SETUP: Usuário {cpf_usuario} já existe.")
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

        try:
            id_sprint_criada = sprint_rep.adicionar_sprint(
                meta = DADOS_SPRINT["meta"],
                inicio = DADOS_SPRINT["inicio"],
                termino = DADOS_SPRINT["termino"],
                revisao_sprint = DADOS_SPRINT["revisao_sprint"],
                id_projeto = id_projeto_criado
            )
            assert id_sprint_criada is not None, "Falha ao obter id_sprint do setup"
            print(f"AVISO SETUP: Sprint {id_sprint_criada} criada.")

        except Exception as e:
            assert False, f"Falha no SETUP (adicionar_sprint): {e}"

        tabela_task = DADOS_TASK.copy()
        tabela_task['id_sprint'] = id_sprint_criada
        tabela_task['cpf'] = cpf_usuario

        response = client.post('/api/tasks/', json = tabela_task)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. "f"Body: {response.get_data(as_text=True)}")
        data = response.get_json()

        id_task_criado = data.get('id_task')
        assert data.get('id_sprint') == id_sprint_criada
        assert data.get('cpf') == cpf_usuario
        assert data.get('descricao_task') == DADOS_TASK['descricao_task']

    finally:

        print("\n--- INICIANDO LIMPEZA ---\n")

        if id_task_criado:
            try:
                task_rep.deletar_task(id_task_criado)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a task {id_task_criado}: {e}")

        if id_sprint_criada:
            try:
                sprint_rep.deletar_sprint(id_sprint_criada)
            except Exception as e:
                print(f"AVISO: Falha ao limpar a sprint {id_sprint_criada}: {e}")

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
