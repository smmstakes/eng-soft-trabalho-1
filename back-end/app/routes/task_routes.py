from ..models import task_rep, sprint_rep, usuario_rep
from flask import Blueprint,request, jsonify

task_bp = Blueprint('task_bp', __name__, url_prefix= '/api/tasks')

@task_bp.route('/', methods = ['POST'])
def criar_task():
    dados = request.json
    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400

    id_sprint = dados.get("id_sprint")
    cpf = dados.get("cpf")
    nome_estado = dados.get("nome_estado")
    descricao_task = dados.get("descricao_task")
    nivel_task = dados.get("nivel_task")

    if not all([id_sprint, cpf, nome_estado, descricao_task, nivel_task]):
        return jsonify({'erro': 'Dados obrigatórios ausentes'}), 400

    try:
        usuario_encontrado = usuario_rep.listar_usuarios(cpf)
        if usuario_encontrado is None :
            raise LookupError("Usuário {cpf} não existe no sistema")

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
        return jsonify({"erro ": str(e)}), 404

    except ValueError as e:
        return jsonify({"erro ": str(e)}), 400

    except ConnectionError as e:
        return jsonify({"erro ": str(e)}), 500

@task_bp.route("/<int:id_task>", methods=["DELETE"])
def deletar_task(id_task):
    try:
        task_encontrada = task_rep.listar_task(id_task=id_task)
        if not task_encontrada:
            return jsonify({"erro": f"Task {id_task} não encontrada"}), 404

        deletado = task_rep.deletar_task(id_task)
        if not deletado:
            raise ConnectionError(f"Falha ao deletar task {id_task}")

        return jsonify({"mensagem": f"Task {id_task} deletada com sucesso"}), 200

    except LookupError as e:
        return jsonify({"erro": str(e)}), 404
    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500
    except Exception as e:
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500