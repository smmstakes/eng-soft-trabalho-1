from ..models import projeto_rep, usuario_rep
from flask import Blueprint,request, jsonify

projeto_bp = Blueprint('projeto_bp', __name__, url_prefix= '/api/projetos')

@projeto_bp.route('/', methods = ['POST'])
def criar_projeto():
    dados = request.json
    
    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400
    
    titulo = dados.get('titulo_projeto')
    descricao = dados.get('descricao')
    cpf_dono = dados.get('cpf')

    if not all([titulo,descricao,cpf_dono]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400
    
    try:

        usuario_encontrado = usuario_rep.listar_usuarios(cpf_dono)
        if usuario_encontrado is None :
            raise LookupError("Usuário {cpf_dono} não existe no sistema")
        
        id_criado = projeto_rep.adicionar_projeto(
            titulo=titulo,
            descricao=descricao,
            cpf_dono=cpf_dono,
        )

        if not id_criado:
            raise ConnectionError(f"Falha em salvar o projeto do Usuário {cpf_dono}")
        

        projeto_criado = projeto_rep.buscar_projeto_por_id(id_criado)

        return jsonify(projeto_criado), 201 
    
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
        
    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500
