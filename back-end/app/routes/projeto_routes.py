from ..models import projeto_rep, usuario_rep, usuario_projeto_rep
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

@projeto_bp.route('/entrar', methods = ['POST'])
@jwt_required()
def entrar_projeto():

    dados = request.json
    cpf_usuario = current_user['cpf']
    id_projeto = dados.get('id_projeto')
    senha = dados.get('senha')
    cargo = dados.get('cargo')

    if cargo != "Dono do Produto":
        cargo = "Desenvolvedor"

    if not all([id_projeto, senha]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400
    
    try:
        dados_projeto = projeto_rep.buscar_projeto_por_id(id_projeto)
        if dados_projeto is None:
            raise LookupError(f"Projeto de id {id_projeto} não existe no sistema")
        
        projetos_usuario = usuario_projeto_rep.listar_projeto_de_usuarios(cpf_usuario)
        for projeto in projetos_usuario:
            if projeto['id_projeto'] == id_projeto:
                raise ValueError(f"Usuário {cpf_usuario} já está em o projeto de id {id_projeto}")

        titulo_projeto = dados_projeto['titulo_projeto']
        cpf_dono = dados_projeto['cpf']
        verificar = projeto_rep.verificar_credenciais_projeto(titulo_projeto, cpf_dono, senha)

        if verificar:
            usuario_projeto_rep.adicionar_usuario_projeto(cpf_usuario, id_projeto, nome_funcao = cargo)

            json = {"id_projeto": id_projeto,
                    "titulo_projeto": titulo_projeto,
                    "cpf":cpf_usuario,
                    "nome_funcao": cargo}
            
            return jsonify(json), 201 
        
    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500
    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
        



