from ..models import projeto_rep, user_story_rep
from flask import Blueprint,request, jsonify

user_story_bp = Blueprint('user_story_bp', __name__, url_prefix='/api/users-stories')

@user_story_bp.route('/', methods=['POST'])
def criar_user_story():
    dados = request.json

    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400

    id_projeto = dados.get('id_projeto')
    titulo_user_story = dados.get('titulo_user_story')
    objetivo = dados.get('objetivo')
    beneficio = dados.get('beneficio')
    prioridade = dados.get('prioridade')

    if not all([id_projeto, titulo_user_story, objetivo, beneficio, prioridade]):
        return jsonify({'erro': 'Dados obrigatórios ausentes.'}), 400

    try:

        projeto_encontrado = projeto_rep.buscar_projeto_por_id(id_projeto)
        if projeto_encontrado is None:
            raise LookupError("Projeto {id_projeto} não existe no sistema.")

        id_user_story_criada = user_story_rep.adicionar_user_story(
            id_projeto = id_projeto,
            titulo_user_story = titulo_user_story,
            objetivo = objetivo,
            beneficio = beneficio,
            prioridade = prioridade
        )

        if not id_user_story_criada:
            raise ConnectionError("Falha em salvar a User_Story do projeto {id_projeto}.")

        user_story_criada = user_story_rep.buscar_user_story_por_id(id_user_story_criada)

        return jsonify(user_story_criada),201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except LookupError as e:
        return jsonify({"erro": str(e)}), 404

    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500

@user_story_bp.route('/<int:user_story_id>', methods=['DELETE'])
def deletar_user_story(user_story_id):
    try:
        user_story_rep.deletar_user_story(user_story_id)
        return jsonify({"mensagem": f"User Story {user_story_id} deletada com sucesso."}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500

    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500