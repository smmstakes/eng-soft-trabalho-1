import sys
import os
import pytest
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from run import create_app
from app.models import usuario_rep, projeto_rep

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
DADOS_PROJETO_TESTE1 = {
    "titulo_projeto": "PROJETO 1 - Joao",
    "descricao": "Teste no banco de dados real",
    "senha": "!MeuProjeto123",
    "cpf": DADOS_USUARIO_DONO['cpf']
}
DADOS_PROJETO_TESTE2 = {
    "titulo_projeto": "PROJETO 2 - Joao",
    "descricao": "Teste rotas do projeto",
    "senha": "!MeuProjeto123",
    "cpf": DADOS_USUARIO_DONO['cpf']
}

def test_criar_projeto_e_limpar(client):
    
    id_projeto_criado = None 
    
    try:

        try:
            usuario_rep.adicionar_usuario(
                cpf=DADOS_USUARIO_DONO["cpf"],
                email=DADOS_USUARIO_DONO["email"],
                nome=DADOS_USUARIO_DONO["nome"],
                senha=DADOS_USUARIO_DONO["senha"]
            )

        except ValueError as e:
            if "já existem" in str(e):
                print(f"AVISO SETUP: Usuário {DADOS_USUARIO_DONO['cpf']} já existe.")
            else:
                assert False, f"Falha no SETUP (adicionar_usuario): {e}"

        login_response = client.post('/api/usuarios/login', json={
            "cpf": DADOS_USUARIO_DONO["cpf"],
            "senha": DADOS_USUARIO_DONO["senha"]
        })

        assert login_response.status_code == 200, "Falha no login do usuário dono do projeto."
        access_token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.post('/api/projetos/', json=DADOS_PROJETO_TESTE1, headers=headers)

        assert response.status_code == 201

        data = response.get_json()

        projetos = projeto_rep.buscar_projetos_por_cpf_dono(DADOS_USUARIO_DONO['cpf'])
        assert projetos and isinstance(projetos, list), f"Nenhum projeto encontrado para CPF {DADOS_USUARIO_DONO['cpf']}"

        projeto = projetos[0]
        assert projeto.get('titulo_projeto') == DADOS_PROJETO_TESTE1['titulo_projeto']
        assert projeto.get('descricao') == DADOS_PROJETO_TESTE1['descricao']
        assert projeto.get('cpf') == DADOS_PROJETO_TESTE1['cpf']

        id_projeto_criado = data.get('id_projeto') or projeto.get('id_projeto')
        assert id_projeto_criado is not None, "Resposta JSON não incluiu 'id_projeto'"

        assert projeto_rep.verificar_credenciais_projeto(
            titulo=DADOS_PROJETO_TESTE1['titulo_projeto'],
            cpf=DADOS_PROJETO_TESTE1['cpf'],
            senha_enviada=DADOS_PROJETO_TESTE1['senha']
        ), "Falha na verificação das credenciais do projeto criado."

        print(f"\nSUCESSO: Projeto {id_projeto_criado} criado.")

    finally:
        
        if id_projeto_criado:
            try:
                projeto_rep.deletar_projeto(id_projeto_criado)

            except Exception as e:
                print(f"AVISO: Falha ao limpar o projeto {id_projeto_criado}: {e}")

        try:
            usuario_rep.deletar_usuario(DADOS_USUARIO_DONO['cpf'])
            print(f"Limpeza: Usuário {DADOS_USUARIO_DONO['cpf']} deletado.")
        except Exception as e:
            print(f"AVISO: Falha ao limpar o usuário {DADOS_USUARIO_DONO['cpf']}: {e}")



def test_listar_projetos_usuario(client):

    try: 
        usuario_rep.adicionar_usuario(
            cpf=DADOS_USUARIO_DONO["cpf"],
            email=DADOS_USUARIO_DONO["email"],
            nome=DADOS_USUARIO_DONO["nome"],
            senha=DADOS_USUARIO_DONO["senha"]
        )

        id_projeto_1 = projeto_rep.adicionar_projeto(
            titulo=DADOS_PROJETO_TESTE1['titulo_projeto'],
            descricao=DADOS_PROJETO_TESTE1['descricao'],
            senha=DADOS_PROJETO_TESTE1['senha'],
            cpf_dono=DADOS_PROJETO_TESTE1['cpf']
        )
        id_projeto_2 = projeto_rep.adicionar_projeto(
            titulo=DADOS_PROJETO_TESTE2['titulo_projeto'],
            descricao=DADOS_PROJETO_TESTE2['descricao'],
            senha=DADOS_PROJETO_TESTE2['senha'],
            cpf_dono=DADOS_PROJETO_TESTE2['cpf']
        )
        
        login_response = client.post('/api/usuarios/login', json={
            "cpf": DADOS_USUARIO_DONO["cpf"],
            "senha": DADOS_USUARIO_DONO["senha"]
        })

        assert login_response.status_code == 200, "Falha no login do usuário dono do projeto."
        access_token = login_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {access_token}'}

        response = client.get('/api/projetos/', headers=headers)

        assert response.status_code == 200

        data = response.get_json()
        assert len(data) == 2

        titulos = {indice.get('titulo_projeto') for indice in data}
        descricoes = {indice.get('descricao') for indice in data}
        cpfs = {indice.get('cpf') for indice in data}
        assert titulos == {DADOS_PROJETO_TESTE1['titulo_projeto'], DADOS_PROJETO_TESTE2['titulo_projeto']}
        assert descricoes == {DADOS_PROJETO_TESTE1['descricao'], DADOS_PROJETO_TESTE2['descricao']}
        assert cpfs == {DADOS_PROJETO_TESTE1['cpf']}
        
    finally:
        try:
            projeto_rep.deletar_projeto(id_projeto_1)
            projeto_rep.deletar_projeto(id_projeto_2)
            usuario_rep.deletar_usuario(DADOS_USUARIO_DONO['cpf'])
        except Exception as e:
            print(f"AVISO: Falha ao limpar dados de teste: {e}")