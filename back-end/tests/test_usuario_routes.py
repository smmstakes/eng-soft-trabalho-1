import sys
import os
import pytest
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from run import create_app 
from app.models import usuario_rep

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

DADOS_USUARIO_DONO = {
    "cpf": "133.446.789-00", 
    "email": "felipeduarte@gmail.com",
    "nome": "Felipe Duarte",
    "senha": "$FelipeDuarte123"}

def test_criar_usuario_e_limpar(client):
    
    try:
        response = client.post('/api/usuarios/', json=DADOS_USUARIO_DONO)

        assert response.status_code == 201
        
        dados= response.get_json()
        assert dados is not None

        cpf_criado = dados.get('cpf')
        token = dados.get('access_token')
        usuario = usuario_rep.listar_usuarios(cpf_criado)[0]

        assert usuario is not None
        assert usuario.get('cpf') == DADOS_USUARIO_DONO['cpf']
        assert usuario.get('nome') == DADOS_USUARIO_DONO['nome']
        assert usuario.get('email') == DADOS_USUARIO_DONO['email']
        assert token is not None

        assert usuario_rep.verificar_credenciais(
            cpf=DADOS_USUARIO_DONO['cpf'], 
            senha_enviada=DADOS_USUARIO_DONO['senha']
        ) is not None
        
    finally:      
        try:
            usuario_rep.deletar_usuario(cpf_criado)
            print(f"Usuário de CPF {cpf_criado} removido com sucesso.")
        except Exception as e:
            print(f"Falha ao limpar usuário de CPF {cpf_criado}: {e}")

def test_login_usuario(client):
    try:
        usuario_rep.adicionar_usuario(
            cpf=DADOS_USUARIO_DONO['cpf'],
            email=DADOS_USUARIO_DONO['email'],
            nome=DADOS_USUARIO_DONO['nome'],
            senha=DADOS_USUARIO_DONO['senha']
        )

        response = client.post('/api/usuarios/login', json={
            "cpf": DADOS_USUARIO_DONO['cpf'],
            "senha": DADOS_USUARIO_DONO['senha']
        })
        assert response.status_code == 200

        dados= response.get_json()
        assert dados is not None

        cpf = dados.get('cpf')
        token = dados.get('access_token')
        assert cpf == DADOS_USUARIO_DONO['cpf']
        assert token is not None

        assert usuario_rep.verificar_credenciais(
            cpf=cpf, 
            senha_enviada=DADOS_USUARIO_DONO['senha']
        )

        assert cpf == DADOS_USUARIO_DONO['cpf']

    finally:
        try:
            usuario_rep.deletar_usuario(DADOS_USUARIO_DONO['cpf'])
            print(f"Usuário de CPF {DADOS_USUARIO_DONO['cpf']} removido com sucesso.")
        except Exception as e:
            print(f"Falha ao limpar usuário de CPF {DADOS_USUARIO_DONO['cpf']}: {e}")