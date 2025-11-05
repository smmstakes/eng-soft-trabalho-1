from ..models import usuario_rep
from flask import Blueprint,request, jsonify
from flask_jwt_extended import create_access_token

usuario_bp = Blueprint('usuario_bp', __name__, url_prefix= '/api/usuarios')

@usuario_bp.route('/', methods = ['POST'])
def criar_usuario():
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400
    
    cpf = dados.get('cpf')
    email = dados.get('email')
    nome = dados.get('nome')
    senha = dados.get('senha')

    if not all([cpf,email,nome,senha]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400
    
    try:
        cpf_criado = usuario_rep.adicionar_usuario(
            cpf=cpf,
            email=email,
            nome=nome,
            senha=senha
        )
        
        if not cpf_criado:
            raise ConnectionError("Falha em salvar o usuário")
        
        access_token = create_access_token(identity=cpf)

        json = {"cpf": cpf_criado,
                "email": email, 
                "nome": nome,
                "access_token": access_token}

        return jsonify(json), 201 
    
    except LookupError as e:
        return jsonify({"erro ": str(e)}), 404
    
    except ValueError as e:
        return jsonify({"erro ": str(e)}), 400
        
    except ConnectionError as e:
        return jsonify({"erro ": str(e)}), 500

@usuario_bp.route('/login', methods = ['POST'])
def login():
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400
    
    cpf = dados.get('cpf')
    senha = dados.get('senha')

    if not all([cpf,senha]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400
    
    try:
        usuario = usuario_rep.verificar_credenciais(cpf, senha)
        access_token = create_access_token(identity=usuario['cpf'])

        json = {"cpf": usuario['cpf'],
                "access_token": access_token}
        
        return jsonify(json), 200
    
    except LookupError as e:
        return jsonify({"erro": str(e)}), 401
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    
    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500