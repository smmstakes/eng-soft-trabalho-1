import datetime
import jwt
from flask import Blueprint, request, jsonify, current_app
from ..models import usuario_rep  # <-- importa tua função

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    secret_key = current_app.config.get('SECRET_KEY')
    if not secret_key:
        return jsonify({'erro': 'SECRET_KEY não configurada'}), 500

    dados = request.get_json()
    cpf = dados.get('cpf')
    senha = dados.get('senha')

    if not cpf or not senha:
        return jsonify({'erro': 'CPF e senha são obrigatórios'}), 400

    try:
        usuario = usuario_rep.verificar_credenciais(cpf, senha)
    except LookupError as e:
        return jsonify({'erro': str(e)}), 401
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

    #Cria token JWT válido por 1 hora (pode incluir dados se quiser)
    payload = {
        'cpf': usuario['cpf'],
        'nome': usuario['nome'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")

    return jsonify({
        'mensagem': f"Bem-vindo, {usuario['nome']}!",
        'token': token
    }), 200
