import sys
import os
import pytest
import json
from typing import Any

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
DADOS_SPRINT: dict[str, Any] = {
    "meta": "Entregar o MVP",
    "inicio": "2025-11-10",
    "termino": "2025-11-20",
    "revisao_sprint": "Revisao ao final do periodo.",
}

def test_criar_sprint_e_limpar(client):
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

        tabela_sprint = DADOS_SPRINT.copy()
        tabela_sprint['id_projeto'] = id_projeto_criado

        response = client.post('/api/sprints/', json = tabela_sprint)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. "f"Body: {response.get_data(as_text=True)}")
        data = response.get_json()

        id_sprint_criada = data.get('id_sprint')
        assert data.get('id_projeto') == id_projeto_criado
        assert data.get('meta') == DADOS_SPRINT['meta']
        assert data.get('inicio') == DADOS_SPRINT['inicio']
        assert data.get('termino') == DADOS_SPRINT['termino']

    finally:
        print("\n--- INICIANDO LIMPEZA ---\n")

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