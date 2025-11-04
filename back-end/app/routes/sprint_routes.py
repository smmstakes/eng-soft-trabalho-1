from ..models import projeto_rep, sprint_rep
from flask import Blueprint,request, jsonify
from datetime import date

sprint_bp = Blueprint('sprint_bp', __name__, url_prefix='/api/sprints')

@sprint_bp.route('/', methods=['POST'])
def criar_sprint():
    dados = request.json

    if not dados:
        return jsonify({'erro': 'JSON ausente'}), 400

    meta = dados.get('meta')
    inicio = dados.get('inicio')
    termino = dados.get('termino')
    revisao_sprint = dados.get('revisao_sprint')
    id_projeto = dados.get('id_projeto')

    if not all([meta, inicio, termino, revisao_sprint, id_projeto]):
        return jsonify({'erro': f'Dados obrigatórios ausentes.'}), 400

    try:

        projeto_encontrado = projeto_rep.buscar_projeto_por_id(id_projeto)
        if projeto_encontrado is None:
            raise LookupError("Projeto {id_projeto} não existe no sistema.")

        id_sprint_criada = sprint_rep.adicionar_sprint(
            meta = meta,
            inicio = inicio,
            termino = termino,
            revisao_sprint = revisao_sprint,
            id_projeto = id_projeto
        )

        if not id_sprint_criada:
            raise ConnectionError("Falha em salvar a Sprint do projeto {id_projeto}")

        sprint_criada = sprint_rep.buscar_sprint_por_id(id_sprint_criada)

        if sprint_criada and isinstance(sprint_criada.get('inicio'), date):
            sprint_criada['inicio'] = sprint_criada['inicio'].isoformat()
        if sprint_criada and isinstance(sprint_criada.get('termino'), date):
            sprint_criada['termino'] = sprint_criada['termino'].isoformat()

        return jsonify(sprint_criada),201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

    except LookupError as e:
        return jsonify({"erro": str(e)}), 404

    except ConnectionError as e:
        return jsonify({"erro": str(e)}), 500