from ..models import projeto_rep, usuario_rep
from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, current_user

projeto_bp = Blueprint('projeto_bp', __name__, url_prefix= '/api/projetos')

@projeto_bp.route('/', methods = ['POST'])
@jwt_required()
def criar_projeto():
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400
    
    titulo = dados.get('titulo_projeto')
    descricao = dados.get('descricao')
    senha = dados.get('senha')
    cpf_dono = current_user['cpf']

    if not all([titulo,descricao,senha]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400
    
    try:

        usuario_encontrado = usuario_rep.listar_usuarios(cpf_dono)
        if usuario_encontrado is None :
            raise LookupError("Usuário {cpf_dono} não existe no sistema")
        
        id_criado = projeto_rep.adicionar_projeto(
            titulo=titulo,
            descricao=descricao,
            senha=senha,
            cpf_dono=cpf_dono
        )

        if not id_criado:
            raise ConnectionError(f"Falha em salvar o projeto do Usuário {cpf_dono}")
        
        json = {"id_projeto": id_criado,
                "titulo_projeto": titulo,
                "descricao": descricao,
                "cpf": cpf_dono}

        return jsonify(json), 201 
    
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
        
    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500

@projeto_bp.route('/', methods = ['GET'])
@jwt_required()
def listar_projetos_usuario():

    try:
        cpf_dono = current_user['cpf']
        projetos = projeto_rep.buscar_projetos_por_cpf_dono(cpf_dono)

        return jsonify(projetos), 200
    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
