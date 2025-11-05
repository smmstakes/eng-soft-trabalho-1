from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.projeto_routes import projeto_bp
from app.routes.user_story_routes import user_story_bp
from app.routes.sprint_routes import sprint_bp
from app.routes.task_routes import task_bp
from app.models.connection import db_path, engine, metadata
from flask_cors import CORS
from app.routes.usuario_routes import usuario_bp
from app.models.usuario_rep import listar_usuarios

def create_app():

    app = Flask(__name__)
    
    CORS(app)
    
    # TODO: Deploy -> Isso não pode ficar exposto aqui usalmente. Precisa estar num .env
    CORS(app, origins="http://localhost:3000")

    app.config["JWT_SECRET_KEY"] = "chave_secreta_para_jwt"
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_data):

        cpf_token = jwt_data["sub"]
        usuario = listar_usuarios(cpf = cpf_token)

        if not usuario:
            return None
        return usuario[0]
    
    app.register_blueprint(projeto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(user_story_bp)
    app.register_blueprint(sprint_bp)
    app.register_blueprint(task_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)