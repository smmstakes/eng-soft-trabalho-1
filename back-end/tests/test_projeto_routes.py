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
DADOS_PROJETO_TESTE = {
    "titulo_projeto": "PROJETO 1 - Joao",
    "descricao": "Teste no banco de dados real",
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

        response = client.post('/api/projetos/', json=DADOS_PROJETO_TESTE)

        assert response.status_code == 201, (
            f"Esperado status 201, obteve {response.status_code}. Body: {response.get_data(as_text=True)}"
        )

        data = response.get_json()

        projetos = projeto_rep.buscar_projetos_por_cpf_dono(DADOS_USUARIO_DONO['cpf'])
        assert projetos and isinstance(projetos, list), f"Nenhum projeto encontrado para CPF {DADOS_USUARIO_DONO['cpf']}"

        projeto = projetos[0]
        assert projeto.get('titulo_projeto') == DADOS_PROJETO_TESTE['titulo_projeto']
        assert projeto.get('descricao') == DADOS_PROJETO_TESTE['descricao']
        assert projeto.get('cpf') == DADOS_PROJETO_TESTE['cpf']

        id_projeto_criado = data.get('id_projeto') or projeto.get('id_projeto')
        assert id_projeto_criado is not None, "Resposta JSON não incluiu 'id_projeto'"

        assert projeto_rep.verificar_credenciais_projeto(
            titulo=DADOS_PROJETO_TESTE['titulo_projeto'],
            cpf=DADOS_PROJETO_TESTE['cpf'],
            senha_enviada=DADOS_PROJETO_TESTE['senha']
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