from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint,request, jsonify
from ..models import task_rep, sprint_rep

task_bp = Blueprint('task_bp', __name__, url_prefix= '/api/tasks')

@task_bp.route('/', methods = ['POST'])
@jwt_required()
def criar_task():
    dados = request.json
    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400

    cpf = get_jwt_identity()

    id_sprint = dados.get("id_sprint")
    nome_estado = dados.get("nome_estado")
    descricao_task = dados.get("descricao_task")
    nivel_task = dados.get("nivel_task")

    if not all([id_sprint, nome_estado, descricao_task, nivel_task]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400

    try:
        sprint_existe = sprint_rep.buscar_sprint_por_id(id_sprint)
        if sprint_existe is None:
            raise LookupError("Sprint {id_sprint} não existe no sistema")

        id_criado = task_rep.adicionar_task(
            id_sprint = id_sprint,
            cpf = cpf,
            nome_estado = nome_estado,
            descricao_task = descricao_task,
            nivel_task = nivel_task
        )

        if not id_criado:
            raise ConnectionError(f"Falha em salvar task do Usuário {cpf}")

        tasks_encontradas = task_rep.listar_task(id_task = id_criado)
        task_criada = tasks_encontradas[0]

        return jsonify(task_criada), 201

    except LookupError as e:
        return jsonify({"erro": str(e)}), 404

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500

@task_bp.route('/', methods=['GET'])
@jwt_required()
def listar_tasks():
    cpf = get_jwt_identity()
    id_sprint = request.args.get("id_sprint")

    try:
        tasks = task_rep.listar_task(cpf = cpf, id_sprint = id_sprint)
        return jsonify(tasks), 200

    except LookupError as e:
        return jsonify({"erro": str(e)}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500