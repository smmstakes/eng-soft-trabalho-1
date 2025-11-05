from flask import request, jsonify, current_app
from functools import wraps
import jwt

def auth_middleware(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        secret_key = current_app.config.get('SECRET_KEY')
        if not secret_key:
            return jsonify({'erro': 'SECRET_KEY não configurada'}), 500

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'erro': 'Token ausente'}), 401

        token = auth_header.split(' ')[1]

        try:
            # apenas valida o token, sem expor dados no request
            jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorator
